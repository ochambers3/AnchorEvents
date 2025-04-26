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
    app.run(debug=True)


if __name__ == "__main__":
    main()


# Things to do:
# The code, as of now, returns blocks without a gap greater than block_size
# Raps and Leafs play back to back from 2024-12-01 to 2024-12-07 so this is one "Block"
# Make city specific/Team specific
# Differentiate between New York Rangers and New York Islanders
# Add comments

# If weekend, only return games with more than one game.
# Print json data well