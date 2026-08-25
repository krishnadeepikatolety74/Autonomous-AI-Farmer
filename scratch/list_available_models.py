import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import google.generativeai as genai
from config import Config

api_key = Config.GEMINI_API_KEY
if api_key:
    genai.configure(api_key=api_key)
    print("Models:")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Name: {m.name}, Display: {m.display_name}")
    except Exception as e:
        print(f"Error listing: {e}")
else:
    print("No API Key configured.")
