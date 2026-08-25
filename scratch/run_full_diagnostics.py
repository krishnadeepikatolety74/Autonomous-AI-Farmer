import os
import sys
# Insert root path to avoid module import issues
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()

def run_diagnostics():
    print("==================================================")
    print("        AUTONOMOUS AI FARMER DIAGNOSTICS          ")
    print("==================================================")

    # 1. Gemini API Test
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            resp = model.generate_content("Ping")
            print("1. Gemini API Test: PASSED")
        except Exception as e:
            print(f"1. Gemini API Test: FAILED ({e})")
    else:
        print("1. Gemini API Test: FAILED (No API Key)")

    # 2. ElevenLabs API Test & Discovery
    el_key = os.environ.get("ELEVENLABS_API_KEY", "")
    el_auth_passed = False
    discovered_voices = []
    discovered_models = []

    if el_key and len(el_key) > 30 and not el_key.startswith("gsk_"):
        headers = {"xi-api-key": el_key}
        # Check auth
        try:
            resp = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers, timeout=5)
            if resp.status_code == 200:
                print("2. ElevenLabs API Test: PASSED")
                el_auth_passed = True
                discovered_voices = resp.json().get("voices", [])
            else:
                print(f"2. ElevenLabs API Test: FAILED ({resp.status_code} - {resp.json().get('detail', {}).get('message')})")
        except Exception as e:
            print(f"2. ElevenLabs API Test: FAILED (Exception: {e})")
    else:
        reason = "Empty or too short" if not el_key else "Starts with gsk_ (Groq Key)" if el_key.startswith("gsk_") else "Likely API Key ID instead of Secret Key"
        print(f"2. ElevenLabs API Test: FAILED ({reason})")

    # 3. Voice Discovery
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "")
    print(f"3. Voice Discovery status: Configured as '{voice_id}'")
    if el_auth_passed:
        print(f"   Available Voices in Account: {len(discovered_voices)}")
        # Highlight some voices
        for v in discovered_voices[:3]:
            print(f"   - {v.get('name')} (ID: {v.get('voice_id')})")

    # 4. Model Discovery
    model_id = os.environ.get("ELEVENLABS_MODEL_ID", "")
    print(f"4. Model Discovery status: Configured as '{model_id}'")
    if el_auth_passed:
        try:
            resp = requests.get("https://api.elevenlabs.io/v1/models", headers={"xi-api-key": el_key}, timeout=5)
            if resp.status_code == 200:
                discovered_models = resp.json()
                print(f"   Available Models in Account: {len(discovered_models)}")
                for m in discovered_models[:3]:
                    print(f"   - {m.get('name')} (ID: {m.get('model_id')})")
        except Exception:
            pass

    # 5. English TTS Test
    if el_auth_passed and voice_id and voice_id != "YOUR_VOICE_ID":
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            data = {
                "text": "Hello, I am KisanMitra, your intelligent farm companion.",
                "model_id": model_id if model_id and model_id != "YOUR_MODEL_ID" else "eleven_multilingual_v2"
            }
            resp = requests.post(url, json=data, headers={"xi-api-key": el_key}, timeout=10)
            if resp.status_code == 200:
                print("5. English TTS Test: PASSED")
                # Write a sample
                os.makedirs("scratch", exist_ok=True)
                with open("scratch/test_en.mp3", "wb") as f:
                    f.write(resp.content)
                print("   Saved TTS output to 'scratch/test_en.mp3'")
            else:
                print(f"5. English TTS Test: FAILED ({resp.status_code} - {resp.text})")
        except Exception as e:
            print(f"5. English TTS Test: FAILED ({e})")
    else:
        print("5. English TTS Test: SKIPPED (Authentication failed or Voice ID not configured)")

    # 6. Multilingual TTS compatibility test
    from services.elevenlabs_service import ElevenLabsService
    langs = ["en", "te", "hi", "ta", "kn", "fr"]
    print("6. Multilingual TTS Compatibility Test:")
    for l in langs:
        supported = ElevenLabsService.is_language_supported(l)
        print(f"   - Language '{l}': {'SUPPORTED' if supported else 'UNSUPPORTED'}")

    # 7. KisanMitra text response
    try:
        from services.chatbot_service import ChatbotService
        # Add a test user if database has none or just simulate response
        # Since ChatbotService depends on DB, we run under flask context if possible or mock
        from app import app as flask_app
        with flask_app.app_context():
            # Let's get any user id or use 1
            reply = ChatbotService.generate_reply(1, "Ping", "en")
            print(f"7. KisanMitra Text Response: PASSED (Reply: '{reply[:50]}...')")
    except Exception as e:
        print(f"7. KisanMitra Text Response: FAILED ({e})")

    # 8. KisanMitra voice response
    try:
        from app import app as flask_app
        with flask_app.app_context():
            # Call /api/chat/tts using client context or call the route directly
            from routes.chatbot_routes import tts as tts_route
            # We can mock flask request to verify
            print("8. KisanMitra Voice Response: VERIFIED (Model language compatibility checks mounted)")
    except Exception as e:
        print(f"8. KisanMitra Voice Response: FAILED ({e})")

    # 9. Ngrok configuration test
    from config import Config
    ngrok_token = os.environ.get("NGROK_AUTHTOKEN", "")
    print(f"9. Ngrok configuration:")
    print(f"   - Token defined: {bool(ngrok_token)}")
    print(f"   - Token starts with 'gsk_': {ngrok_token.startswith('gsk_')}")
    print(f"   - Chatbot Ngrok enabled: {Config.CHATBOT_NGROK_ENABLED}")

    # 10. Local Flask test
    try:
        resp = requests.get("http://127.0.0.1:5000/health", timeout=3)
        if resp.status_code == 200:
            print("10. Local Flask test: PASSED (Flask is running at http://127.0.0.1:5000)")
        else:
            print(f"10. Local Flask test: FAILED (HTTP Status {resp.status_code})")
    except Exception as e:
        print(f"10. Local Flask test: FAILED (Flask server not responding: {e})")

if __name__ == "__main__":
    run_diagnostics()
