import sqlite3
import os
from flask import g, current_app
from config import Config

def get_db():
    """Get database connection for current request context."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize database schemas from schema.sql."""
    db = sqlite3.connect(current_app.config['DATABASE'])
    schema_path = os.path.join(current_app.config['BASE_DIR'], 'database', 'schema.sql')
    
    with open(schema_path, 'r') as f:
        db.executescript(f.read())
    
    db.commit()
    db.close()

def query_db(query, args=(), one=False):
    """Utility to query database and return dictionary lists."""
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Utility to execute insert/update/delete operations."""
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    lastrowid = cur.lastrowid
    cur.close()
    return lastrowid

def init_app(app):
    """Register database hooks with Flask application."""
    app.teardown_appcontext(close_db)

    # Run migration for agent_chat_messages on startup
    with app.app_context():
        try:
            import sqlite3
            db = sqlite3.connect(app.config['DATABASE'])
            db.execute("""
                CREATE TABLE IF NOT EXISTS agent_chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    farm_id INTEGER,
                    agent_name TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    language TEXT DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY(farm_id) REFERENCES farms(id) ON DELETE CASCADE
                )
            """)
            db.commit()
            db.close()
        except Exception as e:
            print(f"Error migrating database: {e}")

