from database import query_db, execute_db

class TaskModel:
    @staticmethod
    def create(user_id, farm_id, task_name, task_type, due_date):
        """Create a new farm task."""
        return execute_db(
            "INSERT INTO farm_tasks (user_id, farm_id, task_name, task_type, due_date, completed) VALUES (?, ?, ?, ?, ?, 0)",
            (user_id, farm_id, task_name.strip(), task_type.strip(), due_date.strip())
        )

    @staticmethod
    def get_all_by_user(user_id):
        """Retrieve all calendar tasks for a user, sorted by due date."""
        rows = query_db(
            "SELECT * FROM farm_tasks WHERE user_id = ? ORDER BY due_date ASC, created_at DESC",
            (user_id,)
        )
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(task_id, user_id):
        """Retrieve a specific task, verifying ownership."""
        row = query_db(
            "SELECT * FROM farm_tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id),
            one=True
        )
        return dict(row) if row else None

    @staticmethod
    def complete(task_id, user_id, completed=1):
        """Mark a task completed or incomplete."""
        execute_db(
            "UPDATE farm_tasks SET completed = ? WHERE id = ? AND user_id = ?",
            (1 if completed else 0, task_id, user_id)
        )

    @staticmethod
    def delete(task_id, user_id):
        """Delete a task."""
        execute_db(
            "DELETE FROM farm_tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id)
        )
