import sqlite3
import os

def migrate_v2():
    db_path = os.path.join('c:\\Users\\kooki\\Desktop\\Farm', 'instance', 'autonomous_farmer.db')
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Create alerts table
    print("Creating 'alerts' table if not exists...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farm_id INTEGER NOT NULL,
        severity TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT DEFAULT 'unread',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(farm_id) REFERENCES farms(id) ON DELETE CASCADE
    )
    """)

    # 2. Create farm_tasks table
    print("Creating 'farm_tasks' table if not exists...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farm_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        farm_id INTEGER,
        task_name TEXT NOT NULL,
        task_type TEXT NOT NULL,
        due_date TEXT NOT NULL,
        completed INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(farm_id) REFERENCES farms(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()
    print("Migration V2 completed successfully!")

if __name__ == "__main__":
    migrate_v2()
