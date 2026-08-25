from database import query_db, execute_db

class RecommendationModel:
    @staticmethod
    def create(farm_id, agent_name, title, description, priority):
        """Add new actionable AI suggestion/recommendation task."""
        rec_id = execute_db(
            """INSERT INTO recommendations 
               (farm_id, agent_name, title, description, priority, completed)
               VALUES (?, ?, ?, ?, ?, 0)""",
            (farm_id, agent_name, title, description, priority)
        )
        return rec_id

    @staticmethod
    def mark_completed(rec_id, farm_id):
        """Toggle recommendation completion state in database."""
        execute_db(
            "UPDATE recommendations SET completed = 1 WHERE id = ? AND farm_id = ?",
            (rec_id, farm_id)
        )

    @staticmethod
    def get_active(farm_id):
        """Retrieve uncompleted suggestions list."""
        rows = query_db(
            "SELECT * FROM recommendations WHERE farm_id = ? AND completed = 0 ORDER BY created_at DESC",
            (farm_id,)
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_all(farm_id, limit=50):
        """Retrieve complete suggestions list (completed and pending)."""
        rows = query_db(
            "SELECT * FROM recommendations WHERE farm_id = ? ORDER BY completed ASC, created_at DESC LIMIT ?",
            (farm_id, limit)
        )
        return [dict(row) for row in rows]

    @staticmethod
    def clear_active_by_agent(farm_id, agent_name):
        """Clear active/uncompleted suggestions created by a specific agent."""
        execute_db(
            "DELETE FROM recommendations WHERE farm_id = ? AND agent_name = ? AND completed = 0",
            (farm_id, agent_name)
        )

    @staticmethod
    def update_texts(rec_id, title, description):
        """Update recommendation title and description."""
        execute_db(
            "UPDATE recommendations SET title = ?, description = ? WHERE id = ?",
            (title, description, rec_id)
        )
