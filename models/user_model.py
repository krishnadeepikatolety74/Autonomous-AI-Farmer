from werkzeug.security import generate_password_hash, check_password_hash
from database import query_db, execute_db

class UserModel:
    @staticmethod
    def create(name, email, password, language='en'):
        """Create new user with hashed password."""
        password_hash = generate_password_hash(password)
        try:
            user_id = execute_db(
                "INSERT INTO users (name, email, password_hash, language) VALUES (?, ?, ?, ?)",
                (name, email, password_hash, language)
            )
            return user_id
        except Exception as e:
            # Handle unique constraint violations
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def find_by_email(email):
        """Find user by email address."""
        row = query_db("SELECT * FROM users WHERE email = ?", (email,), one=True)
        return dict(row) if row else None

    @staticmethod
    def find_by_id(user_id):
        """Find user by ID."""
        row = query_db("SELECT * FROM users WHERE id = ?", (user_id,), one=True)
        return dict(row) if row else None

    @staticmethod
    def verify_password(stored_hash, password):
        """Verify password against hashed value."""
        return check_password_hash(stored_hash, password)

    @staticmethod
    def update_language(user_id, language):
        """Update user preferences language."""
        execute_db("UPDATE users SET language = ? WHERE id = ?", (language, user_id))

    @staticmethod
    def update_profile(user_id, name, email):
        """Update user profile name and email."""
        execute_db("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))

    @staticmethod
    def email_exists(email, exclude_user_id=None):
        """Check if an email already exists in the database, optionally excluding a user ID."""
        if exclude_user_id:
            row = query_db("SELECT id FROM users WHERE email = ? AND id != ?", (email, exclude_user_id), one=True)
        else:
            row = query_db("SELECT id FROM users WHERE email = ?", (email,), one=True)
        return row is not None

    @staticmethod
    def update_password(user_id, password):
        """Hash and update the password for the given user."""
        password_hash = generate_password_hash(password)
        execute_db("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, user_id))

    @staticmethod
    def update_preferences(user_id, language, voice_responses, auto_play_voice, voice):
        """Update all voice and language preferences for the user."""
        execute_db(
            "UPDATE users SET language = ?, voice_responses = ?, auto_play_voice = ?, voice = ? WHERE id = ?",
            (language, 1 if voice_responses else 0, 1 if auto_play_voice else 0, voice, user_id)
        )
