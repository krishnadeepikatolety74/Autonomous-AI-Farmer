from database import query_db, execute_db

class QuickNoteModel:
    @staticmethod
    def create(user_id, farm_id, note):
        """Create a new quick note for the user."""
        return execute_db(
            "INSERT INTO quick_notes (user_id, farm_id, note, completed) VALUES (?, ?, ?, 0)",
            (user_id, farm_id, note.strip())
        )

    @staticmethod
    def get_all_by_user(user_id):
        """Retrieve all quick notes for a given user."""
        rows = query_db(
            "SELECT * FROM quick_notes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_incomplete_by_user(user_id, limit=None):
        """Retrieve incomplete quick notes, with an optional limit."""
        query = "SELECT * FROM quick_notes WHERE user_id = ? AND completed = 0 ORDER BY created_at DESC"
        if limit:
            query += f" LIMIT {int(limit)}"
        rows = query_db(query, (user_id,))
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(note_id, user_id):
        """Retrieve a specific note by ID, verifying ownership."""
        row = query_db(
            "SELECT * FROM quick_notes WHERE id = ? AND user_id = ?",
            (note_id, user_id),
            one=True
        )
        return dict(row) if row else None

    @staticmethod
    def complete(note_id, user_id, completed=1):
        """Mark a quick note as completed or incomplete, securing by user_id."""
        execute_db(
            "UPDATE quick_notes SET completed = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
            (1 if completed else 0, note_id, user_id)
        )

    @staticmethod
    def delete(note_id, user_id):
        """Delete a quick note, securing by user_id."""
        execute_db(
            "DELETE FROM quick_notes WHERE id = ? AND user_id = ?",
            (note_id, user_id)
        )

    @staticmethod
    def clear_completed(user_id):
        """Delete all completed quick notes for the user."""
        execute_db(
            "DELETE FROM quick_notes WHERE user_id = ? AND completed = 1",
            (user_id,)
        )
