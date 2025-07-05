# conftest.py (place in /backend/tests/)
import pytest
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from config import TestingConfig
from utils.db import get_db, init_db

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