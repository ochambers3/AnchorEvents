from flask import Flask, request, jsonify, g
from datetime import datetime
from service.game_service import GameService
from repository.db_setup import init_db
import sqlite3


class GameController:

    def __init__(self, db, app):
        self.db = db
        self.app = app
        self.service = GameService(db)
        self.setup_routes()

    def setup_routes(self):
    
        #Route using today's date and city. Default start-date is today.
        @self.app.route('/date-city', methods=['POST'])
        def get_date_team():
            db = init_db()
            data = request.json

            games = self.service.get_games(db, data)
            # print(games)
            # print("jsonifying")
            # print(jsonify(games))
            return jsonify(games), 200
        
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
        
        @self.app.route('/weighted-date', methods=['POST'])
        def get_weighted_date():
            db = self.get_db()
            data = request.json
            nfl_weight = data.get("nfl_weight")
            nba_weight = data.get("nba_weight")
            nhl_weight = data.get("nhl_weight")
            selected_leagues = ("NFL", "NBA", "NHL")
            start_date = data.get("start_date")
            end_date = data.get("end_date")

            if not all([nfl_weight, nba_weight, nhl_weight, selected_leagues, start_date, end_date]):
                return jsonify({'error': 'Missing required data'}), 400

            games = self.service.get_games_by_leagues(nfl_weight, nba_weight, nhl_weight, selected_leagues, start_date, end_date, self.db)
            return jsonify(games), 200
        


