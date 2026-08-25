import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database import query_db

app = create_app()

with app.app_context():
    users = query_db("SELECT id, name, email, language FROM users")
    for u in users:
        print(f"ID: {u['id']}, Name: {u['name']}, Email: {u['email']}, Lang: {u['language']}")
