import sys
import os

# Add parent directory to path so we can import local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from database import query_db
from services.recommendation_service import RecommendationService

app = create_app()

with app.app_context():
    recs_before = query_db("SELECT * FROM recommendations WHERE completed = 0")
    
    # Test translate to Telugu
    print("Running translation function to Telugu ('te') for Farm 3...")
    try:
        RecommendationService.translate_active_recommendations(3, 'te')
        print("Translation function executed successfully.")
    except Exception as e:
        print(f"Translation execution failed: {e}")

    recs_after = query_db("SELECT * FROM recommendations WHERE completed = 0")

# Write to log file with UTF-8
with open("scratch/translation_test_output.txt", "w", encoding="utf-8") as f:
    f.write("=== BEFORE ===\n")
    for r in recs_before:
        f.write(f"ID: {r['id']}, FarmID: {r['farm_id']}, Title: {r['title']}, Desc: {r['description']}\n")
    f.write("\n=== AFTER ===\n")
    for r in recs_after:
        f.write(f"ID: {r['id']}, FarmID: {r['farm_id']}, Title: {r['title']}, Desc: {r['description']}\n")

print("Wrote results to scratch/translation_test_output.txt")
