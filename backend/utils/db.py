import sqlite3
import os
from flask import g

# Define the path to the database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database', 'schedule.db')
TEST_DB_OVERRIDE = None

def get_db():
    """Get the database connection for the current request."""
    if TEST_DB_OVERRIDE:
        return TEST_DB_OVERRIDE  # ← use test connection if provided'

    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row  # Enable dict-like access to rows
    return g.db

def close_db(e=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the database with required tables."""
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    # Use a direct connection for initialization (not Flask g)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            game_id INTEGER PRIMARY KEY,
            league TEXT NOT NULL,
            date DATE NOT NULL,
            time DATETIME,
            artist TEXT,
            team_away TEXT,
            team_home TEXT,
            venue TEXT,
            city TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add indexes for better query performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_date ON events(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_city ON events(city)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_events_league ON events(league)')
    
    conn.commit()
    conn.close()

def init_app(app):
    """Initialize the database with the Flask app."""
    app.teardown_appcontext(close_db)
    
    # Initialize database tables
    with app.app_context():
        init_db()