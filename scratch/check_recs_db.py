import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database import query_db

app = create_app()

with app.app_context():
    rows = query_db("SELECT id, farm_id, agent_name, title, completed FROM recommendations")
    with open("scratch/db_recs_check.txt", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(f"ID: {r['id']}, FarmID: {r['farm_id']}, Agent: {r['agent_name']}, Completed: {r['completed']}, Title: {r['title']}\n")

print("Done checking.")
