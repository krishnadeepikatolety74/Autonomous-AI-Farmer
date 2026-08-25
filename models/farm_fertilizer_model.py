from database import query_db, execute_db

# The 7 approved fertilizers
FERTILIZER_LIST = [
    'Urea',
    'DAP',
    'MOP / Potash',
    'SSP',
    'NPK 10:26:26',
    'NPK 19:19:19',
    'Ammonium Sulphate',
]

class FarmFertilizerModel:

    @staticmethod
    def ensure_table():
        """Create the farm_fertilizers table if it doesn't exist."""
        execute_db("""
            CREATE TABLE IF NOT EXISTS farm_fertilizers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                farm_id INTEGER NOT NULL UNIQUE,
                fertilizer_data TEXT NOT NULL DEFAULT '{}',
                notes TEXT DEFAULT '',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(farm_id) REFERENCES farms(id) ON DELETE CASCADE
            )
        """)

    @staticmethod
    def save(farm_id, fertilizer_data: dict, notes: str = ''):
        """Save or update the fertilizer usage for a farm.
        fertilizer_data: {fertilizer_name: {"value": number, "unit": "kg" or "%"}, ...}
        """
        import json
        FarmFertilizerModel.ensure_table()
        existing = query_db(
            "SELECT id FROM farm_fertilizers WHERE farm_id = ?",
            (farm_id,), one=True
        )
        data_json = json.dumps(fertilizer_data)
        if existing:
            execute_db(
                "UPDATE farm_fertilizers SET fertilizer_data = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE farm_id = ?",
                (data_json, notes, farm_id)
            )
        else:
            execute_db(
                "INSERT INTO farm_fertilizers (farm_id, fertilizer_data, notes) VALUES (?, ?, ?)",
                (farm_id, data_json, notes)
            )

    @staticmethod
    def get(farm_id):
        """Return dict {fertilizer_name: dose_kg_per_ha} for a farm, or empty dict."""
        import json
        try:
            FarmFertilizerModel.ensure_table()
            row = query_db(
                "SELECT fertilizer_data, notes FROM farm_fertilizers WHERE farm_id = ?",
                (farm_id,), one=True
            )
            if row:
                return {
                    'fertilizers': json.loads(row['fertilizer_data'] or '{}'),
                    'notes': row['notes'] or ''
                }
        except Exception:
            pass
        return {'fertilizers': {}, 'notes': ''}
