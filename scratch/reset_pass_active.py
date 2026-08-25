import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_app
from database import execute_db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    h = generate_password_hash('password')
    rows = execute_db("UPDATE users SET password_hash = ? WHERE email = ?", (h, 'user@example.com'))
    print(f"Password reset for user@example.com. Rows affected: {rows}")
