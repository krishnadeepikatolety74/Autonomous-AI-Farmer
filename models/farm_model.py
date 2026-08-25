from database import query_db, execute_db

class FarmModel:
    @staticmethod
    def create_or_update(user_id, name, location, area, soil_type, irrigation_method):
        """Save or update farm profiles belonging to a user ID."""
        existing = FarmModel.get_by_user_id(user_id)
        if existing:
            execute_db(
                "UPDATE farms SET name = ?, location = ?, area = ?, soil_type = ?, irrigation_method = ? WHERE user_id = ?",
                (name, location, area, soil_type, irrigation_method, user_id)
            )
            return existing['id']
        else:
            farm_id = execute_db(
                "INSERT INTO farms (user_id, name, location, area, soil_type, irrigation_method) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, name, location, area, soil_type, irrigation_method)
            )
            return farm_id

    @staticmethod
    def get_by_user_id(user_id):
        """Get farm details linked to user ID."""
        row = query_db("SELECT * FROM farms WHERE user_id = ?", (user_id,), one=True)
        return dict(row) if row else None

    @staticmethod
    def get_by_id(farm_id):
        """Get farm details linked to farm ID."""
        row = query_db("SELECT * FROM farms WHERE id = ?", (farm_id,), one=True)
        return dict(row) if row else None
