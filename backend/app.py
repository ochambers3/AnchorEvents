from flask import Flask
from flask_cors import CORS
from game_controller import GameController
from utils.db import init_app
from api.filter_data import FilterData
from config import DevelopmentConfig, TestingConfig, Config
import os

def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        env = os.getenv('FLASK_ENV', 'development')
        if env == 'testing':
            app.config.from_object(TestingConfig)
        elif env == 'development':
            app.config.from_object(DevelopmentConfig)
        else:
            app.config.from_object(Config)
    else:
        app.config.from_object(config)
    
    # Initialize CORS
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

    # Initialize database
    init_app(app)

    # Initialize controllers
    GameController(app)

    # Initialize API data population (consider moving this to a CLI command)
    with app.app_context():
        populate_initial_data()

    return app

def populate_initial_data():
    """Populate database with initial data from APIs."""
    from utils.db import get_db
    
    # Only populate if database is empty (optional check)
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM events')
    count = cursor.fetchone()[0]
    
    if count == 0:  # Only populate if empty
        api = FilterData(db)
        # api.nba_filter()
        # api.nhl_filter()
        # api.nfl_filter()
        # api.ticketmaster_concert_filter(['New York', 'Chicago', 'Dallas', 'Los Angeles', 'Miami', 'Boston', 'Nashville'])
        api.ticketmaster_concert_filter(['Dallas'], 1)

def main():
    """Main entry point for the application."""
    app = create_app()
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    main()