from database import query_db, execute_db

class ObservationModel:
    @staticmethod
    def add(farm_id, soil_moisture, soil_ph, nitrogen, phosphorus, potassium,
            temperature, humidity, rainfall, crop_health, disease_notes=None, market_price=0.0):
        """Insert new daily observation telemetry dataset associated with a farm."""
        observation_id = execute_db(
            """INSERT INTO observations 
               (farm_id, soil_moisture, soil_ph, nitrogen, phosphorus, potassium, 
                temperature, humidity, rainfall, crop_health, disease_notes, market_price)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (farm_id, soil_moisture, soil_ph, nitrogen, phosphorus, potassium,
             temperature, humidity, rainfall, crop_health, disease_notes, market_price)
        )
        return observation_id

    @staticmethod
    def get_latest(farm_id):
        """Retrieve most recent observation metrics for a farm."""
        row = query_db(
            "SELECT * FROM observations WHERE farm_id = ? ORDER BY observed_at DESC LIMIT 1",
            (farm_id,),
            one=True
        )
        return dict(row) if row else None

    @staticmethod
    def get_all(farm_id, limit=20):
        """Retrieve historical observation logs list."""
        rows = query_db(
            "SELECT * FROM observations WHERE farm_id = ? ORDER BY observed_at DESC LIMIT ?",
            (farm_id, limit)
        )
        return [dict(row) for row in rows]
