from datetime import datetime
from repository.game_repository import GameRepository


class GameService:
    """Service layer for game-related operations."""

    def __init__(self):
        """Initialize the game service."""
        self.repository = GameRepository()

    def get_games(self, db, filters):
        """Get games based on the provided filters.
        
        Args:
            db: Database connection
            filters: Dictionary containing filter parameters:
                - start_date: Optional start date (YYYY-MM-DD)
                - end_date: Optional end date (YYYY-MM-DD)
                - cities: Optional list of city names
                - weekdays: Optional list of weekday numbers (0=Monday, 6=Sunday)
        
        Returns:
            Dictionary of games organized by date and city, only including
            cities with more than one game on the specified weekdays
        """
        # Extract filter parameters
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')
        cities = filters.get('cities', [])
        weekdays = filters.get('weekdays', [])  # List of weekday numbers (0-6)

        # Get games from repository
        games = self.repository.get_games(
            db,
            start_date=start_date,
            end_date=end_date,
            cities=cities if cities else None
        )

        # Filter by weekdays if specified
        if weekdays:
            games = [
                game for game in games
                if datetime.strptime(game['date'], '%Y-%m-%d').weekday() in weekdays
            ]

        # Organize games by date and city
        organized_games = {}
        city_game_counts = {}  # Track number of games per city

        for game in games:
            date = game['date']
            city = game['city']
            
            # Initialize nested structures if they don't exist
            if date not in organized_games:
                organized_games[date] = {}
            if city not in organized_games[date]:
                organized_games[date][city] = []
            
            # Add game to the organization
            organized_games[date][city].append(game)
            
            # Track city game count
            if city not in city_game_counts:
                city_game_counts[city] = 0
            city_game_counts[city] += 1

        # Filter out cities with only one game
        filtered_games = {}
        for date, cities_dict in organized_games.items():
            filtered_cities = {
                city: games_list
                for city, games_list in cities_dict.items()
                if city_game_counts[city] > 1
            }
            if filtered_cities:  # Only include dates that have cities with multiple games
                filtered_games[date] = filtered_cities

        return filtered_games