import os
import re
import requests
from config import Config

# Standard fallbacks for ElevenLabs models language support
MODEL_LANGUAGES_FALLBACK = {
    'eleven_multilingual_v2': {'en', 'de', 'pl', 'es', 'it', 'fr', 'pt', 'hi', 'te', 'ta', 'kn', 'ja', 'zh', 'ko', 'ru', 'tr', 'nl', 'sv', 'no', 'da', 'fi', 'cs', 'el', 'uk', 'ms', 'id', 'vi', 'ro', 'hu'},
    'eleven_multilingual_v1': {'en', 'de', 'pl', 'es', 'it', 'fr', 'pt', 'hi', 'zh', 'ja', 'ko', 'ru'},
    'eleven_monolingual_v1': {'en'}
}

class ElevenLabsService:
    @staticmethod
    def update_env_value(key, value):
        """Safely write/update key-value pair in .env file."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        env_path = os.path.join(base_dir, '.env')
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            content = ""

        pattern = rf"^{key}\s*=.*"
        replacement = f"{key}={value}"
        if re.search(pattern, content, re.MULTILINE):
            new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        else:
            new_content = content.rstrip() + f"\n{key}={value}\n"

        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

    @classmethod
    def discover_and_update_env(cls):
        """Automatically query the ElevenLabs API to find available voices and models,
        select the best ones, and update the .env file.
        """
        api_key = Config.ELEVENLABS_API_KEY
        if not api_key or len(api_key) < 30 or api_key.startswith("gsk_"):
            return {
                "success": False,
                "error": "ElevenLabs API key is missing or invalid."
            }

        headers = {"xi-api-key": api_key}
        
        # 1. Discover Models
        models_url = "https://api.elevenlabs.io/v1/models"
        selected_model = None
        try:
            resp = requests.get(models_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                models = resp.json()
                # Try to find eleven_multilingual_v2
                for model in models:
                    if model.get("model_id") == "eleven_multilingual_v2":
                        selected_model = model
                        break
                # If not found, look for any multilingual model
                if not selected_model:
                    for model in models:
                        if "multilingual" in model.get("model_id", "").lower():
                            selected_model = model
                            break
                # Fallback to first model
                if not selected_model and models:
                    selected_model = models[0]
            else:
                pass  # silently ignore models fetch failure
        except Exception:
            pass

        # 2. Discover Voices
        voices_url = "https://api.elevenlabs.io/v1/voices"
        selected_voice_id = None
        selected_voice_name = None
        try:
            resp = requests.get(voices_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                voices_data = resp.json()
                voices = voices_data.get("voices", [])
                
                # We want a warm, clear, professional voice.
                premade_voices = [v for v in voices if v.get("category") == "premade"]
                # Try to find Rachel
                rachel = next((v for v in premade_voices if v.get("name") == "Rachel"), None)
                if rachel:
                    selected_voice_id = rachel.get("voice_id")
                    selected_voice_name = rachel.get("name")
                else:
                    for v in premade_voices:
                        desc = str(v.get("description", "")).lower()
                        if any(word in desc for word in ["warm", "clear", "friendly", "professional", "conversational"]):
                            selected_voice_id = v.get("voice_id")
                            selected_voice_name = v.get("name")
                            break
                    if not selected_voice_id and premade_voices:
                        selected_voice_id = premade_voices[0].get("voice_id")
                        selected_voice_name = premade_voices[0].get("name")
                    if not selected_voice_id and voices:
                        selected_voice_id = voices[0].get("voice_id")
                        selected_voice_name = voices[0].get("name")
        except Exception:
            pass

        updates = {}
        if selected_model:
            model_id = selected_model.get("model_id")
            cls.update_env_value("ELEVENLABS_MODEL_ID", model_id)
            updates["ELEVENLABS_MODEL_ID"] = model_id
        if selected_voice_id:
            cls.update_env_value("ELEVENLABS_VOICE_ID", selected_voice_id)
            updates["ELEVENLABS_VOICE_ID"] = selected_voice_id
            
        return {
            "success": bool(updates),
            "updates": updates,
            "voice_name": selected_voice_name
        }

    @classmethod
    def is_language_supported(cls, language):
        """Check if the given language code is supported by the configured model."""
        model_id = Config.ELEVENLABS_MODEL_ID or 'eleven_multilingual_v2'
        
        # 1. First, try dynamic check if key is available
        api_key = Config.ELEVENLABS_API_KEY
        if api_key and len(api_key) > 30 and not api_key.startswith("gsk_"):
            try:
                url = "https://api.elevenlabs.io/v1/models"
                headers = {"xi-api-key": api_key}
                resp = requests.get(url, headers=headers, timeout=5)
                if resp.status_code == 200:
                    models = resp.json()
                    for model in models:
                        if model.get("model_id") == model_id:
                            langs = {l.get("language_id") for l in model.get("languages", [])}
                            return language in langs
            except Exception:
                pass
                
        # 2. Fallback to hardcoded list
        supported = MODEL_LANGUAGES_FALLBACK.get(model_id, MODEL_LANGUAGES_FALLBACK['eleven_multilingual_v2'])
        return language in supported

    @classmethod
    def text_to_speech(cls, text, voice_id=None, language='en'):
        """
        Convert text message content to speech audio data using ElevenLabs API.
        Returns bytes of the MP3 audio if successful, None otherwise.
        """
        api_key = Config.ELEVENLABS_API_KEY
        if not api_key or api_key.startswith("gsk_"):
            print("ElevenLabs API key is not configured or invalid.")
            return None

        # Verify language support
        if not cls.is_language_supported(language):
            print(f"Language '{language}' is not supported by model '{Config.ELEVENLABS_MODEL_ID}'")
            return None

        voice_to_use = voice_id or Config.ELEVENLABS_VOICE_ID or '21m00Tcm4TlvDq8ikWAM'
        model_to_use = Config.ELEVENLABS_MODEL_ID or 'eleven_multilingual_v2'
        
        # Clean text slightly
        clean_text = text.replace('**', '').replace('*', '').replace('#', '').replace('`', '')

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_to_use}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": clean_text,
            "model_id": model_to_use,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        try:
            resp = requests.post(url, json=data, headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.content
            else:
                print(f"ElevenLabs API error: {resp.status_code} - {resp.text}")
                return None
        except Exception as e:
            print(f"Exception during ElevenLabs text-to-speech: {e}")
            return None
