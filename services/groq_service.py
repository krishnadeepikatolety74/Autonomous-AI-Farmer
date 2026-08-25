from groq import Groq
from config import Config

class GroqService:
    @classmethod
    def generate_response(cls, prompt, system_instruction=None, lang_code=None):
        """Query Groq API for text completion."""
        api_key = Config.GROQ_API_KEY
        if not api_key:
            return "Groq API key is not configured. Please check the server settings."

        # Setup target language directive in prompt
        if lang_code:
            from services.language_service import LanguageService
            directive = LanguageService.get_language_directive(lang_code)
            prompt += f"\n\nIMPORTANT: {directive}"
            if system_instruction:
                system_instruction += f" {directive}"

        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        # Try a list of standard Groq models
        models_to_try = ["qwen/qwen3.6-27b", "openai/gpt-oss-20b", "openai/gpt-oss-120b"]
        last_err = None
        
        for model in models_to_try:
            try:
                client = Groq(api_key=api_key)
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7,
                )
                if response and response.choices and len(response.choices) > 0:
                    try:
                        from utils.api_usage import increment_api_usage
                        increment_api_usage("groq")
                    except Exception:
                        pass
                    content = response.choices[0].message.content or ""
                    # Strip <think>...</think> reasoning blocks (e.g. Qwen models)
                    import re
                    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL).strip()
                    if content:
                        return content
                    # If stripping left nothing, skip to next model
                    continue
            except Exception as e:
                last_err = str(e)
                print(f"Groq API error with model {model}: {e}")
                import traceback
                traceback.print_exc()
                continue


        return f"Groq API invocation failed: {last_err or 'No response choices available.'}"
