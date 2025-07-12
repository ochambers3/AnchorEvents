# conftest.py (place in /backend/tests/)
import pytest
import sys
import os
import json
from pathlib import Path
import sqlite3

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from config import TestingConfig
from utils.db import get_db, init_db
from utils import db as db_utils

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app(TestingConfig)  # Use testing config
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Create database for testing."""
    with app.app_context():
        init_db()
        yield get_db()

@pytest.fixture
def test_db():
    # Create in-memory SQLite DB
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row

    # Set the override
    db_utils.TEST_DB_OVERRIDE = conn

    # Initialize schema
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE events (
            game_id INTEGER PRIMARY KEY,
            league TEXT NOT NULL,
            date DATE NOT NULL,
            time DATETIME,
            team_away TEXT NOT NULL,
            team_home TEXT NOT NULL,
            venue TEXT,
            city TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()

    yield conn

    # Teardown
    conn.close()
    db_utils.TEST_DB_OVERRIDE = None

@pytest.fixture
def sample_concert_data():
    path = Path(__file__).parent / "sample_ticketmaster.json"
    with open(path) as f:
        return json.load(f)