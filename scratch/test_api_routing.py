import sys
import os
import json
import time

# Ensure base directory is on path
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_dir)

# Set stdout encoding
sys.stdout.reconfigure(encoding='utf-8')

from app import create_app
from database import query_db, execute_db
from utils.api_usage import get_api_usage, reset_api_usage
from config import Config

def redact_key(key):
    if not key:
        return "Not Set"
    if len(key) <= 12:
        return "***"
    return f"{key[:6]}...{key[-6:]}"

def test_routing_and_usage():
    print("==================================================")
    print("      API ROUTING & CALL COUNT VERIFICATION       ")
    print("==================================================")

    # 1. Initialize Flask app
    app = create_app()
    client = app.test_client()

    with app.app_context():
        # Get or create a test user
        user = query_db("SELECT * FROM users LIMIT 1", one=True)
        if not user:
            print("No users found in database, creating a test user...")
            # Insert a dummy user
            user_id = execute_db(
                "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                ("Test Farmer", "testfarmer@kisan.com", "dummy_hash")
            )
            user = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
        
        user_id = user['id']
        print(f"Using test user: {user['name']} (ID: {user_id})")

        # Confirm Config values (redacted)
        print(f"GEMINI_API_KEY loaded: {redact_key(Config.GEMINI_API_KEY)}")
        print(f"GROQ_API_KEY loaded:  {redact_key(Config.GROQ_API_KEY)}")

        if not Config.GROQ_API_KEY:
            print("ERROR: GROQ_API_KEY is not set. Cannot run Groq tests.")
            sys.exit(1)
        if not Config.GEMINI_API_KEY:
            print("ERROR: GEMINI_API_KEY is not set. Cannot run Gemini tests.")
            sys.exit(1)

        # Ensure a farm exists for the test user so the prompt context loads successfully
        farm = query_db("SELECT * FROM farms WHERE user_id = ?", (user_id,), one=True)
        if not farm:
            print("Creating test farm for user...")
            execute_db(
                "INSERT INTO farms (user_id, name, location, area, soil_type, irrigation_method) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, "Green Fields", "Hyderabad", 5.0, "Loamy", "Drip")
            )

        # 2. Reset call counts to start from 0
        reset_api_usage()
        initial_usage = get_api_usage()
        print(f"\nInitial call count statistics: {initial_usage}")
        assert initial_usage["groq_calls"] == 0, "Groq call counter did not reset to 0"
        assert initial_usage["gemini_calls"] == 0, "Gemini call counter did not reset to 0"

        # 3. Simulate calling KisanMitra chatbot (/api/chat)
        print("\n--- Testing KisanMitra Chat Endpoint (/api/chat) -> Groq ---")
        with client.session_transaction() as sess:
            sess['user_id'] = user_id

        # Make request to KisanMitra /api/chat
        payload_chat = {
            "message": "What is the primary crop recommendation for my farm?",
            "language": "en"
        }
        start_time = time.time()
        response_chat = client.post('/api/chat', json=payload_chat)
        elapsed_chat = time.time() - start_time

        print(f"Response Status: {response_chat.status_code}")
        response_data_chat = json.loads(response_chat.data.decode('utf-8'))
        print(f"Response Success Field: {response_data_chat.get('success')}")
        print(f"KisanMitra Reply: {response_data_chat.get('message')}")
        print(f"Request elapsed: {elapsed_chat:.2f} seconds")

        # Verify call counts after chat call
        post_chat_usage = get_api_usage()
        print(f"Call count statistics after KisanMitra request: {post_chat_usage}")
        
        # Verify Groq was called and Gemini was NOT
        if response_chat.status_code == 200 and response_data_chat.get('success') is True:
            print("KisanMitra request succeeded!")
            assert post_chat_usage["groq_calls"] > 0, "Groq calls did not increase!"
            assert post_chat_usage["gemini_calls"] == 0, "Gemini was incorrectly invoked during KisanMitra call!"
            print("VERIFICATION SUCCESS: KisanMitra used Groq, Gemini usage remained 0.")
        else:
            print("ERROR: KisanMitra request failed.")
            sys.exit(1)

        # 4. Simulate calling Specialist Agent chat (/api/agent-chat)
        print("\n--- Testing Specialist Agent Endpoint (/api/agent-chat) -> Gemini ---")
        payload_agent = {
            "agent": "weather",
            "message": "How does the weather forecast look for the next few days?",
            "language": "en"
        }
        start_time = time.time()
        response_agent = client.post('/api/agent-chat', json=payload_agent)
        elapsed_agent = time.time() - start_time

        print(f"Response Status: {response_agent.status_code}")
        response_data_agent = json.loads(response_agent.data.decode('utf-8'))
        print(f"Response Success Field: {response_data_agent.get('success')}")
        print(f"Agent Reply: {response_data_agent.get('message')}")
        print(f"Request elapsed: {elapsed_agent:.2f} seconds")

        # Verify call counts after agent call
        post_agent_usage = get_api_usage()
        print(f"Call count statistics after Agent request: {post_agent_usage}")

        # Verify Gemini was called and Groq call count stayed unchanged (isolated)
        if response_agent.status_code == 200 and response_data_agent.get('success') is True:
            print("Specialist Agent request succeeded!")
            assert post_agent_usage["gemini_calls"] > 0, "Gemini calls did not increase!"
            assert post_agent_usage["groq_calls"] == post_chat_usage["groq_calls"], "Groq was incorrectly invoked during Agent call!"
            print("VERIFICATION SUCCESS: Specialist Agent used Gemini, Groq usage remained unchanged.")
        else:
            print("ERROR: Specialist Agent request failed.")
            sys.exit(1)

        print("\n==================================================")
        print("          ALL VERIFICATIONS PASSED!               ")
        print("==================================================")

if __name__ == "__main__":
    test_routing_and_usage()
