import os
import json
import re
import google.generativeai as genai
from config import Config
from services.language_service import LanguageService

class GeminiService:
    _configured = False

    @classmethod
    def _configure_api(cls):
        """Configure the Gemini API client from settings."""
        if not cls._configured:
            api_key = Config.GEMINI_API_KEY
            if api_key:
                try:
                    genai.configure(api_key=api_key)
                    cls._configured = True
                except Exception as e:
                    print(f"Error configuring Gemini client: {e}")
            else:
                print("Warning: GEMINI_API_KEY not found in configuration. Mock data fallbacks will be used.")

    @classmethod
    def generate_json(cls, prompt, system_instruction=None, fallback_mock=None, lang_code=None):
        """
        Request text completion from Gemini, expecting a JSON response.
        Falls back to fallback_mock if error or parsing fails.
        """
        cls._configure_api()

        # Determine target language code
        active_lang = lang_code
        if not active_lang:
            from flask import has_request_context, g
            if has_request_context() and hasattr(g, 'user') and g.user and g.user.get('language'):
                active_lang = g.user['language']

        if active_lang:
            target_lang = LanguageService.get_language_name(active_lang)
            directive = LanguageService.get_language_directive(active_lang)
            language_directive = (
                f"\n\nIMPORTANT: {directive} "
                f"You MUST write all user-facing text fields (such as 'summary', 'recommendation', "
                f"'title', 'description', 'reasoning', 'final_plan', 'overall_status') in {target_lang}. "
                f"Do NOT translate key names/JSON structures, only translate their string values."
            )
            prompt += language_directive
            if system_instruction:
                system_instruction += f" Write all output text values in {target_lang}."

        if not cls._configured:
            print("Gemini API not configured. Returning fallback mock data.")
            return fallback_mock or {"error": "AI service temporarily unavailable."}

        try:
            # Use the configured model (or fall back to gemini-3.5-flash)
            model_name = getattr(Config, 'GEMINI_MODEL', 'gemini-3.5-flash') or 'gemini-3.5-flash'
            
            # Setup generation configuration
            generation_config = {
                "response_mime_type": "application/json"
            }
            
            # Create model instance
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                system_instruction=system_instruction
            )
            
            # Send prompt
            response = model.generate_content(prompt)
            if not response or not hasattr(response, 'text') or not response.text:
                raise ValueError("Empty or invalid response from Gemini API.")
            
            try:
                from utils.api_usage import increment_api_usage
                increment_api_usage("gemini")
            except Exception:
                pass
            
            # Extract content text and clean markdown blocks if returned
            text = response.text.strip()
            # Clean ```json block formatting if API didn't strip it (handles arrays and objects)
            array_match = re.search(r'\[.*\]', text, re.DOTALL)
            object_match = re.search(r'\{.*\}', text, re.DOTALL)
            
            if array_match and (not object_match or array_match.start() < object_match.start()):
                text = array_match.group(0)
            elif object_match:
                text = object_match.group(0)
                
            return json.loads(text)
            
        except Exception as e:
            print(f"Gemini API invocation failure: {e}")
            if fallback_mock:
                print("Returning fallback mock data due to API error.")
                return fallback_mock
            return {"error": "AI service temporarily unavailable. Please try again."}

    @classmethod
    def generate_response(cls, prompt, system_instruction=None, lang_code=None):
        """Regular text generation wrapper."""
        cls._configure_api()

        # Inject language directive into prompt when a preferred language is set
        active_lang = lang_code
        if not active_lang:
            from flask import has_request_context, g
            if has_request_context() and hasattr(g, 'user') and g.user and g.user.get('language'):
                active_lang = g.user['language']

        if active_lang:
            directive = LanguageService.get_language_directive(active_lang)
            prompt += f"\n\nIMPORTANT: {directive}"
            if system_instruction:
                system_instruction += f" {directive}"

        if not cls._configured:
            return "AI service temporarily unavailable."
        try:
            model_name = getattr(Config, 'GEMINI_MODEL', 'gemini-3.5-flash') or 'gemini-3.5-flash'
            model = genai.GenerativeModel(model_name, system_instruction=system_instruction)
            response = model.generate_content(prompt)
            if not response or not hasattr(response, 'text') or not response.text:
                return "AI service temporarily unavailable."
            try:
                from utils.api_usage import increment_api_usage
                increment_api_usage("gemini")
            except Exception:
                pass
            return response.text
        except Exception as e:
            print(f"Gemini API text invocation failure: {e}")
            return "AI service temporarily unavailable."

    @classmethod
    def generate_from_image(cls, image_bytes, mime_type, prompt, system_instruction=None, lang_code=None):
        """Send an image alongside a text prompt to Gemini (Multimodal) — returns JSON string."""
        cls._configure_api()

        # Determine target language code
        active_lang = lang_code
        if not active_lang:
            from flask import has_request_context, g
            if has_request_context() and hasattr(g, 'user') and g.user and g.user.get('language'):
                active_lang = g.user['language']

        if active_lang:
            target_lang = LanguageService.get_language_name(active_lang)
            directive = LanguageService.get_language_directive(active_lang)
            language_directive = (
                f"\n\nIMPORTANT: {directive} "
                f"You MUST write all user-facing text values (crop name, issue description, cause, symptoms, "
                f"recommendations, prevention, explanation, missing_information) in {target_lang}. "
                f"Do NOT translate JSON key names. Only translate their string values. "
                f"Ensure all returned values are fully written in {target_lang}."
            )
            prompt += language_directive
            if system_instruction:
                system_instruction += f" Write all output text values in {target_lang}."

        if not cls._configured:
            print("[GeminiService] API not configured — cannot run image analysis.")
            return "AI service temporarily unavailable."
        try:
            image_part = {
                "mime_type": mime_type,
                "data": image_bytes
            }
            model_name = getattr(Config, 'GEMINI_MODEL', 'gemini-2.0-flash') or 'gemini-2.0-flash'
            
            # Use JSON response mime type for reliable structured output
            generation_config = {
                "response_mime_type": "application/json"
            }
            
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config=generation_config,
                system_instruction=system_instruction
            )
            response = model.generate_content([prompt, image_part])
            
            # Validate response
            if not response:
                print("[GeminiService] Vision: received None response")
                return "AI service temporarily unavailable."
            
            # Check for blocked content (safety filters)
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                block_reason = getattr(response.prompt_feedback, 'block_reason', None)
                if block_reason:
                    print(f"[GeminiService] Vision: response blocked — {block_reason}")
                    return "AI service temporarily unavailable."
            
            if not hasattr(response, 'text') or not response.text:
                print("[GeminiService] Vision: empty text in response")
                return "AI service temporarily unavailable."
            
            try:
                from utils.api_usage import increment_api_usage
                increment_api_usage("gemini")
            except Exception:
                pass
            return response.text
        except Exception as e:
            print(f"[GeminiService] Vision API error: {e}")
            return "AI service temporarily unavailable. Please try again."

