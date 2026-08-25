import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-autonomous-farmer')
    
    # Base Directories
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # SQLite Database Configuration
    INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    DATABASE = os.path.join(INSTANCE_DIR, 'autonomous_farmer.db')
    
    # Gemini API Key
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash')
    
    # Groq API Key
    _raw_groq = os.environ.get('GROQ_API_KEY', '').strip()
    if not _raw_groq:
        _raw_ngrok = os.environ.get('NGROK_AUTHTOKEN', '').strip()
        if _raw_ngrok.startswith('gsk_'):
            _raw_groq = _raw_ngrok
    GROQ_API_KEY = _raw_groq

    
    # Translation Directory
    TRANSLATIONS_DIR = os.path.join(BASE_DIR, 'translations')

    # Ngrok configuration for external tunnel access
    _raw_ngrok_token = os.environ.get('NGROK_AUTHTOKEN', '').strip()
    NGROK_AUTHTOKEN = '' if _raw_ngrok_token.startswith('gsk_') else _raw_ngrok_token
    NGROK_URL = os.environ.get('NGROK_URL', '')
    CHATBOT_NGROK_ENABLED = (
        os.environ.get('CHATBOT_NGROK_ENABLED', 'False').lower() in ('true', '1')
        and bool(NGROK_AUTHTOKEN)
    )

    # ElevenLabs Text-to-Speech API
    ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY', '')
    ELEVENLABS_VOICE_ID = os.environ.get('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM') # Default voice (Rachel)
    ELEVENLABS_MODEL_ID = os.environ.get('ELEVENLABS_MODEL_ID', 'eleven_multilingual_v2') # Default multilingual model

    # Open-Meteo Live Weather (free, no API key required)
    # Set OPENMETEO_ENABLED=false in .env to disable live weather fetching
    OPENMETEO_ENABLED = os.environ.get('OPENMETEO_ENABLED', 'true').lower() in ('true', '1', 'yes')
