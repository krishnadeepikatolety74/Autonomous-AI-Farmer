from database import query_db, execute_db

class AgentChatModel:
    @staticmethod
    def add_message(user_id, farm_id, agent_name, role, message, language='en'):
        """Insert an agent chat message record."""
        return execute_db(
            """INSERT INTO agent_chat_messages (user_id, farm_id, agent_name, role, message, language)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, farm_id, agent_name, role, message, language)
        )

    @staticmethod
    def get_history(user_id, farm_id, agent_name, limit=20):
        """Retrieve recent chat history for a user, farm, and specific agent."""
        if farm_id:
            rows = query_db(
                """SELECT * FROM agent_chat_messages 
                   WHERE user_id = ? AND agent_name = ? AND (farm_id = ? OR farm_id IS NULL)
                   ORDER BY created_at DESC LIMIT ?""",
                (user_id, agent_name, farm_id, limit)
            )
        else:
            rows = query_db(
                """SELECT * FROM agent_chat_messages 
                   WHERE user_id = ? AND agent_name = ? AND farm_id IS NULL
                   ORDER BY created_at DESC LIMIT ?""",
                (user_id, agent_name, limit)
            )
        messages = [dict(row) for row in rows]
        messages.reverse()
        return messages

    @staticmethod
    def clear_history(user_id, farm_id, agent_name):
        """Delete all chat logs for user/farm/agent context."""
        if farm_id:
            execute_db(
                "DELETE FROM agent_chat_messages WHERE user_id = ? AND agent_name = ? AND (farm_id = ? OR farm_id IS NULL)",
                (user_id, agent_name, farm_id)
            )
        else:
            execute_db(
                "DELETE FROM agent_chat_messages WHERE user_id = ? AND agent_name = ? AND farm_id IS NULL",
                (user_id, agent_name)
            )
