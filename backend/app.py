import sqlite3
from flask import Flask, g
from flask_cors import CORS
from controller.game_controller import GameController
from utils.db import close_db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)

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