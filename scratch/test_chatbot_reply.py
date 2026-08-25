import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from services.chatbot_service import ChatbotService

app = create_app()

with app.app_context():
    print("Generating chatbot reply for Telugu user...")
    # Mocking user_id=1, query="పంటలకు ఎలాంటి ఎరువులు వేయాలి?", language="te"
    reply = ChatbotService.generate_reply(user_id=1, message="పంటలకు ఎలాంటి ఎరువులు వేయాలి?", language="te")
    
    # Save output to a file using UTF-8 to avoid console print errors
    with open("scratch/chatbot_reply_test_output.txt", "w", encoding="utf-8") as f:
        f.write(f"USER: పంటలకు ఎలాంటి ఎరువులు వేయాలి?\n")
        f.write(f"CHATBOT REPLY:\n{reply}\n")

print("Done! Reply saved to scratch/chatbot_reply_test_output.txt")
