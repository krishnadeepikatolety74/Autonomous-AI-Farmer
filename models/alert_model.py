from database import query_db, execute_db

class AlertModel:
    @staticmethod
    def create(farm_id, severity, title, description):
        """Create a new smart alert for a farm."""
        return execute_db(
            "INSERT INTO alerts (farm_id, severity, title, description, status) VALUES (?, ?, ?, ?, 'unread')",
            (farm_id, severity.upper(), title.strip(), description.strip())
        )

    @staticmethod
    def get_all_by_farm(farm_id):
        """Retrieve all alerts for a given farm, sorted by time."""
        rows = query_db(
            "SELECT * FROM alerts WHERE farm_id = ? ORDER BY created_at DESC",
            (farm_id,)
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_unread_by_farm(farm_id):
        """Retrieve only unread alerts for a farm."""
        rows = query_db(
            "SELECT * FROM alerts WHERE farm_id = ? AND status = 'unread' ORDER BY created_at DESC",
            (farm_id,)
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id_and_user(alert_id, user_id):
        """Fetch alert by ID ensuring ownership verification."""
        row = query_db(
            """SELECT a.* FROM alerts a 
               JOIN farms f ON a.farm_id = f.id 
               WHERE a.id = ? AND f.user_id = ?""",
            (alert_id, user_id),
            one=True
        )
        return dict(row) if row else None

    @staticmethod
    def mark_as_read(alert_id, farm_id):
        """Mark an alert as read."""
        execute_db(
            "UPDATE alerts SET status = 'read' WHERE id = ? AND farm_id = ?",
            (alert_id, farm_id)
        )

    @staticmethod
    def dismiss(alert_id, farm_id):
        """Mark an alert as dismissed."""
        execute_db(
            "UPDATE alerts SET status = 'dismissed' WHERE id = ? AND farm_id = ?",
            (alert_id, farm_id)
        )

    @staticmethod
    def delete(alert_id, farm_id):
        """Delete an alert."""
        execute_db(
            "DELETE FROM alerts WHERE id = ? AND farm_id = ?",
            (alert_id, farm_id)
        )
