import sys
import os
import json

# Ensure base directory is on path
project_dir = r"c:\Users\kooki\Desktop\Autonomous AI Farme"
sys.path.insert(0, project_dir)

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

from app import create_app
from database import query_db
from services.chatbot_service import ChatbotService
from config import Config

app = create_app()

def test_kisanmitra():
    with app.app_context():
        # Get a test user
        user = query_db("SELECT * FROM users LIMIT 1", one=True)
        if not user:
            print("ERROR: No test user found in database.")
            return
            
        user_id = user['id']
        print(f"Testing KisanMitra Groq Integration for user: {user['name']} (ID {user_id})")
        print(f"Resolving GROQ_API_KEY from config...")
        key = Config.GROQ_API_KEY
        if key:
            print(f"GROQ_API_KEY successfully resolved! (Length: {len(key)})")
            # Redact the key to not print it
            masked = key[:6] + "..." + key[-6:]
            print(f"Masked key: {masked}")
        else:
            print("ERROR: GROQ_API_KEY could not be resolved.")
            return

        message = "Hello KisanMitra, can you summarize the primary goal of our farm based on my profile?"
        print(f"\nSending message to KisanMitra companion chat: '{message}'")
        
        try:
            # We measure time and result
            import time
            start = time.time()
            reply = ChatbotService.generate_reply(user_id, message, language='en')
            elapsed = time.time() - start
            
            print(f"\nResponse received in {elapsed:.2f} seconds:")
            print("-" * 60)
            print(reply)
            print("-" * 60)
            
            if reply and "not configured" not in reply and "invocation failed" not in reply and "Sorry, I couldn't" not in reply:
                print("\nSUCCESS: KisanMitra successfully completed a Groq API request!")
            else:
                print("\nFAILURE: Request returned fallback or error state.")
        except Exception as e:
            import traceback
            print(f"\nFAILURE: Exception raised: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    test_kisanmitra()
