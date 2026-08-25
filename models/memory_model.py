from database import query_db, execute_db

class MemoryModel:
    @staticmethod
    def add(farm_id, plan_summary, risk_assessment):
        """Append a new historical snapshot of farm plan context to memory."""
        memory_id = execute_db(
            "INSERT INTO farm_memory (farm_id, plan_summary, risk_assessment) VALUES (?, ?, ?)",
            (farm_id, plan_summary, risk_assessment)
        )
        return memory_id

    @staticmethod
    def get_recent(farm_id, limit=5):
        """Get recent plan summaries to feeds as context parameters for agents."""
        rows = query_db(
            "SELECT * FROM farm_memory WHERE farm_id = ? ORDER BY created_at DESC LIMIT ?",
            (farm_id, limit)
        )
        return [dict(row) for row in rows]
