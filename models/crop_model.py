from database import query_db, execute_db

class CropModel:
    @staticmethod
    def create_or_update(farm_id, name, variety, planting_date, stage):
        """Save or update primary crop associated with a farm ID."""
        existing = CropModel.get_by_farm_id(farm_id)
        if existing:
            execute_db(
                "UPDATE crops SET name = ?, variety = ?, planting_date = ?, stage = ? WHERE farm_id = ?",
                (name, variety, planting_date, stage, farm_id)
            )
            return existing['id']
        else:
            crop_id = execute_db(
                "INSERT INTO crops (farm_id, name, variety, planting_date, stage) VALUES (?, ?, ?, ?, ?)",
                (farm_id, name, variety, planting_date, stage)
            )
            return crop_id

    @staticmethod
    def get_by_farm_id(farm_id):
        """Get crop details linked to farm ID."""
        row = query_db("SELECT * FROM crops WHERE farm_id = ?", (farm_id,), one=True)
        return dict(row) if row else None
