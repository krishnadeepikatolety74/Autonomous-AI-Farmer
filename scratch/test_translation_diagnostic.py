import sys
import os
import traceback
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database import query_db
from models.recommendation_model import RecommendationModel
import google.generativeai as genai
from config import Config

app = create_app()

error_msg = "No error"

with app.app_context():
    try:
        # Run raw generation directly to inspect the exact exception
        api_key = Config.GEMINI_API_KEY
        genai.configure(api_key=api_key)
        
        farm_id = 3
        target_lang = "Telugu"
        recs = RecommendationModel.get_active(farm_id)
        
        items_to_translate = []
        for r in recs:
            items_to_translate.append({
                "id": r["id"],
                "title": r["title"],
                "description": r["description"]
            })

        prompt = (
            f"You are a professional agricultural translator. "
            f"Please translate the following recommendation list into {target_lang}. "
            f"You MUST keep the IDs intact and only translate the 'title' and 'description' fields.\n\n"
            f"Recommendations:\n{json.dumps(items_to_translate, ensure_ascii=False)}\n\n"
            f"Output a strict JSON array matching the input structure: "
            f"[ {{\"id\": id, \"title\": \"translated title\", \"description\": \"translated description\"}} ]"
        )

        print("Sending generation request...")
        model = genai.GenerativeModel(
            "gemini-3.5-flash",
            generation_config={"response_mime_type": "application/json"},
            system_instruction=f"You are an expert translator. Translate titles and descriptions of agricultural recommendations into {target_lang}."
        )
        response = model.generate_content(prompt)
        print(f"Raw response text: {response.text}")
        
        text = response.text.strip()
        import re
        array_match = re.search(r'\[.*\]', text, re.DOTALL)
        object_match = re.search(r'\{.*\}', text, re.DOTALL)
        
        if array_match and (not object_match or array_match.start() < object_match.start()):
            text = array_match.group(0)
        elif object_match:
            text = object_match.group(0)
            
        data = json.loads(text)
        print(f"Successfully decoded JSON: {len(data)} items.")
        
    except Exception as e:
        error_msg = f"Exception: {str(e)}\nTraceback:\n{traceback.format_exc()}"

with open("scratch/translation_error.txt", "w", encoding="utf-8") as f:
    f.write(error_msg)

print("Done diagnostic run.")
