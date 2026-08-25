from database import query_db, execute_db

class ChatModel:
    @staticmethod
    def add_message(user_id, farm_id, role, message, language='en'):
        """Insert a chat message record."""
        return execute_db(
            """INSERT INTO chat_messages (user_id, farm_id, role, message, language)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, farm_id, role, message, language)
        )

    @staticmethod
    def get_history(user_id, farm_id, limit=20):
        """Retrieve recent chat history limit for a user/farm context."""
        # Clean up database variables context if farm_id is None
        if farm_id:
            rows = query_db(
                """SELECT * FROM chat_messages 
                   WHERE user_id = ? AND (farm_id = ? OR farm_id IS NULL)
                   ORDER BY created_at DESC LIMIT ?""",
                (user_id, farm_id, limit)
            )
        else:
            rows = query_db(
                """SELECT * FROM chat_messages 
                   WHERE user_id = ? AND farm_id IS NULL
                   ORDER BY created_at DESC LIMIT ?""",
                (user_id, limit)
            )
        # Return in ascending order (oldest first) so they display in order
        messages = [dict(row) for row in rows]
        messages.reverse()
        return messages

    @staticmethod
    def clear_history(user_id, farm_id):
        """Delete all chat logs for user/farm context."""
        if farm_id:
            execute_db(
                "DELETE FROM chat_messages WHERE user_id = ? AND (farm_id = ? OR farm_id IS NULL)",
                (user_id, farm_id)
            )
        else:
            execute_db(
                "DELETE FROM chat_messages WHERE user_id = ? AND farm_id IS NULL",
                (user_id,)
            )
