import os
import sys
import unittest
import sqlite3
import io

# Setup imports path
sys.path.append('c:\\Users\\kooki\\Desktop\\Farm')

from app import create_app
from models.alert_model import AlertModel
from models.task_model import TaskModel
from services.alert_service import AlertService
from services.calendar_service import CalendarService
from services.report_service import ReportService

class TestFinalPhase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        self.user_id = 3 # Test user id
        self.farm_id = 1 # Test farm id

    def test_alerts_crud(self):
        print("\n--- Testing Alerts CRUD ---")
        # 1. Create alert
        alert_id = AlertModel.create(
            farm_id=self.farm_id,
            severity='HIGH',
            title='Test Soil Alert',
            description='This is a verification alert.'
        )
        self.assertIsNotNone(alert_id)
        print(f"Created alert with ID: {alert_id}")

        # 2. Get alerts
        alerts = AlertModel.get_all_by_farm(self.farm_id)
        self.assertTrue(len(alerts) > 0)
        found = any(a['id'] == alert_id for a in alerts)
        self.assertTrue(found)

        # 3. Mark read
        AlertModel.mark_as_read(alert_id, self.farm_id)
        alerts_unread = AlertModel.get_unread_by_farm(self.farm_id)
        found_unread = any(a['id'] == alert_id for a in alerts_unread)
        self.assertFalse(found_unread)
        print("Alert mark_as_read verified.")

        # 4. Clean up
        AlertModel.delete(alert_id, self.farm_id)
        print("Alert delete verified.")

    def test_tasks_crud(self):
        print("\n--- Testing Tasks CRUD ---")
        # 1. Create task
        task_id = TaskModel.create(
            user_id=self.user_id,
            farm_id=self.farm_id,
            task_name='Inspect Tomato Leaves',
            task_type='Disease Inspection',
            due_date='2026-08-15'
        )
        self.assertIsNotNone(task_id)
        print(f"Created task with ID: {task_id}")

        # 2. Get tasks
        tasks = TaskModel.get_all_by_user(self.user_id)
        self.assertTrue(len(tasks) > 0)
        found = any(t['id'] == task_id for t in tasks)
        self.assertTrue(found)

        # 3. Complete task
        TaskModel.complete(task_id, self.user_id, completed=1)
        task = TaskModel.get_by_id(task_id, self.user_id)
        self.assertEqual(task['completed'], 1)
        print("Task complete toggle verified.")

        # 4. Clean up
        TaskModel.delete(task_id, self.user_id)
        tasks_after = TaskModel.get_all_by_user(self.user_id)
        found_after = any(t['id'] == task_id for t in tasks_after)
        self.assertFalse(found_after)
        print("Task delete verified.")

    def test_report_generation(self):
        print("\n--- Testing PDF Report Generation ---")
        mock_farm = {'id': 1, 'name': 'Green Orchard', 'location': 'Pune', 'area': 15.5, 'soil_type': 'Loam', 'irrigation_method': 'Drip'}
        mock_crop = {'name': 'Tomato', 'variety': 'Cherry', 'planting_date': '2026-05-10', 'stage': 'Flowering'}
        mock_obs = {'soil_moisture': 35.2, 'soil_ph': 6.5, 'nitrogen': 40.0, 'phosphorus': 30.0, 'potassium': 50.0, 'temperature': 28.5, 'humidity': 62.0, 'rainfall': 5.0, 'crop_health': 88.0, 'market_price': 2200}
        mock_recs = [{'title': 'Water Crop', 'description': 'Soil moisture is low.', 'priority': 'High', 'agent_name': 'Irrigation Agent'}]
        mock_alerts = [{'severity': 'HIGH', 'title': 'High Temp', 'description': 'Temp above 35C'}]
        mock_runs = []

        pdf_stream = ReportService.generate_pdf(
            farm=mock_farm,
            crop=mock_crop,
            observation=mock_obs,
            recommendations=mock_recs,
            alerts=mock_alerts,
            recent_runs=mock_runs,
            final_plan=None
        )
        self.assertIsNotNone(pdf_stream)
        self.assertTrue(len(pdf_stream.getvalue()) > 100)
        print(f"Generated PDF successfully. Byte length: {len(pdf_stream.getvalue())}")

if __name__ == "__main__":
    unittest.main()
