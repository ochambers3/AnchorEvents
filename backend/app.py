import sqlite3
from flask import Flask, g
from flask_cors import CORS
from controller.game_controller import GameController
from utils.db import close_db
from api.filter_data import FilterData
from repository.db_setup import init_db

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

        # Create an application context
    with app.app_context():
        # Get the database instance
        db = init_db()

        #Passing database to api to get data
        api = FilterData(db)
        api.nba_filter()
        api.nhl_filter()
        api.nfl_filter()

    # Pass the db instance to the controller as well
    # controller = GameController(db, app)

    # Initialize controllers
    GameController(app)

    # Register database cleanup
    close_db(app)

    return app


def main():
    """Main entry point for the application."""
    app = create_app()
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    main()