import sys
import os
import traceback
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
import google.generativeai as genai
from config import Config

app = create_app()

error_msg = "No error"

with app.app_context():
    try:
        api_key = Config.GEMINI_API_KEY
        genai.configure(api_key=api_key)
        
        print("Testing gemini-3.5-flash with JSON mime type...")
        generation_config = {
            "response_mime_type": "application/json"
        }
        model = genai.GenerativeModel(
            "gemini-3.5-flash",
            generation_config=generation_config
        )
        response = model.generate_content("Respond with a JSON object containing a 'msg' field with value 'hello'")
        print(f"Response: {response.text}")
        
    except Exception as e:
        error_msg = f"Exception: {str(e)}\nTraceback:\n{traceback.format_exc()}"

with open("scratch/translation_error.txt", "w", encoding="utf-8") as f:
    f.write(error_msg)

print("Done JSON gemini run.")
