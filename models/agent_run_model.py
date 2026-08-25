from database import query_db, execute_db

class AgentRunModel:
    @staticmethod
    def record(farm_id, agent_name, status, risk_level, confidence, run_time, output_json=None):
        """Save a new agent run log."""
        run_id = execute_db(
            """INSERT INTO agent_runs 
               (farm_id, agent_name, status, risk_level, confidence, run_time, output_json)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (farm_id, agent_name, status, risk_level, confidence, run_time, output_json)
        )
        return run_id

    @staticmethod
    def get_latest_by_agent(farm_id, agent_name):
        """Get latest agent run result."""
        row = query_db(
            "SELECT * FROM agent_runs WHERE farm_id = ? AND agent_name = ? ORDER BY created_at DESC LIMIT 1",
            (farm_id, agent_name),
            one=True
        )
        return dict(row) if row else None

    @staticmethod
    def get_all(farm_id, limit=30):
        """Get all historical agent run executions for timeline feeds."""
        rows = query_db(
            "SELECT * FROM agent_runs WHERE farm_id = ? ORDER BY created_at DESC LIMIT ?",
            (farm_id, limit)
        )
        return [dict(row) for row in rows]
