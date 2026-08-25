from datetime import datetime, timedelta
from models.task_model import TaskModel

class CalendarService:
    @staticmethod
    def generate_tasks_from_recommendations(user_id, farm_id, recommendations):
        """
        Extract tasks from plan recommendations and insert them
        into the calendar schedule table.
        """
        tasks_created = 0
        if not recommendations:
            return tasks_created

        # Map agent names to task types
        agent_type_map = {
            'Weather Agent': 'Weather Review',
            'Soil Agent': 'Soil Check',
            'Crop Disease Agent': 'Disease Inspection',
            'Irrigation Agent': 'Irrigation',
            'Fertilizer Agent': 'Fertilizer Check',
            'Market Agent': 'Market Review',
            'Farm Planning Agent': 'Plan Review'
        }

        # Set default task due date to tomorrow
        due_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

        for rec in recommendations:
            task_name = rec.get('title')
            agent_name = rec.get('agent_name', 'Farm Planning Agent')
            task_type = agent_type_map.get(agent_name, 'Other')

            # Create task
            TaskModel.create(
                user_id=user_id,
                farm_id=farm_id,
                task_name=task_name,
                task_type=task_type,
                due_date=due_date
            )
            tasks_created += 1

        return tasks_created
