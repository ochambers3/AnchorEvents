from flask import request, jsonify
from datetime import datetime
from service.game_service import GameService
from utils.db import get_db


class GameController:
    """Controller for handling game-related routes."""

    def __init__(self, app):
        """Initialize the controller with Flask app and set up routes.
        
        Args:
            app: Flask application instance
        """
        self.app = app
        self.service = GameService()
        self.setup_routes()

    def setup_routes(self):
        """Set up the routes for the game controller."""
        
        #Route using today's date and city. Default start-date is today.
        @self.app.route('/date-city', methods=['POST'])
        def get_games():
            """Handle POST requests to /date-city endpoint.
            
            Expects JSON payload with optional fields:
            - start_date: Start date for game search (YYYY-MM-DD)
            - end_date: End date for game search (YYYY-MM-DD)
            - city: City name to filter games by
            - weekdays: List of weekdays to filter games by
            
            Returns:
                JSON response with games organized by date and city
            """
            try:
                data = request.json
                db = get_db()
                games = self.service.get_games(db, data)
                return jsonify(games), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        # Test route
        @self.app.route('/test', methods=['POST'])
        def get_test():
            data = {
            "2024-10-18": {
                "Chicago": [
                {
                    "date": "2024-10-18",
                    "id": 12400070,
                    "league": "NBA",
                    "team_away": "Cleveland Cavaliers",
                    "team_home": "Chicago Bulls",
                    "time": "2024-10-18T19:00:00",
                    "venue": "United Center"
                },
                {
                    "date": "2024-10-19",
                    "id": 2024020085,
                    "league": "NHL",
                    "team_away": "Buffalo Sabres",
                    "team_home": "Chicago Blackhawks",
                    "time": "2024-10-19 19:00:00",
                    "venue": "United Center"
                }
                ],
                "Winnipeg": [
                {
                    "date": "2024-10-18",
                    "id": 2024020073,
                    "league": "NHL",
                    "team_away": "San Jose Sharks",
                    "team_home": "Winnipeg Jets",
                    "time": "2024-10-18 19:00:00",
                    "venue": "Canada Life Centre"
                },
                {
                    "date": "2024-10-20",
                    "id": 2024020088,
                    "league": "NHL",
                    "team_away": "Pittsburgh Penguins",
                    "team_home": "Winnipeg Jets",
                    "time": "2024-10-20 14:00:00",
                    "venue": "Canada Life Centre"
                }
                ]
            },
            "2024-10-25": {
            "Chicago": [
                {
                "date": "2024-10-25",
                "id": 2024020120,
                "league": "NHL",
                "team_away": "Nashville Predators",
                "team_home": "Chicago Blackhawks",
                "time": "2024-10-25 19:30:00",
                "venue": "United Center"
                },
                {
                "date": "2024-10-26",
                "id": 22400091,
                "league": "NBA",
                "team_away": "Oklahoma City Thunder",
                "team_home": "Chicago Bulls",
                "time": "2024-10-26T19:00:00",
                "venue": "United Center"
                }
            ],
            "Cleveland": [
                {
                "date": "2024-10-25",
                "id": 22400080,
                "league": "NBA",
                "team_away": "Detroit Pistons",
                "team_home": "Cleveland Cavaliers",
                "time": "2024-10-25T19:30:00",
                "venue": "Rocket Mortgage FieldHouse"
            }]}}
            return jsonify(data), 200
