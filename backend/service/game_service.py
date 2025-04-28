from datetime import datetime, timedelta
from repository.game_repository import GameRepository
from itertools import groupby
from operator import itemgetter


class GameService:
    """Service layer for game-related operations."""

    def __init__(self):
        """Initialize the game service."""
        self.repository = GameRepository()

    def _get_week_range(self, date_str):
        """Get the week range for a given date based on weekday filter."""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.strftime('%Y-%m-%d')

    def get_games(self, db, filters):
        """Get games based on the provided filters.
        
        Args:
            db: Database connection
            filters: Dictionary containing filter parameters:
                - start_date: Optional start date (YYYY-MM-DD)
                - end_date: Optional end date (YYYY-MM-DD)
                - cities: Optional list of city names
                - weekdays: Optional list of weekday numbers (0=Monday, 6=Sunday)
                          Must be a contiguous range (e.g., [0,1,2] for Mon-Wed)
        
        Returns:
            If weekdays specified:
                Dictionary organized by week ranges, then by cities
            If no weekdays specified:
                Dictionary organized by individual dates, then by cities
        """
        # Extract filter parameters
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')
        cities = filters.get('cities', [])
        weekdays = sorted(filters.get('weekdays', []))  # List of weekday numbers (0-6)

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

        # First, count games per city to filter out single-game cities
        city_games = {}
        for game in games:
            city = game['city']
            if city not in city_games:
                city_games[city] = []
            city_games[city].append(game)

        cities_with_multiple_games = {
            city for city, games_list in city_games.items()
            if len(games_list) > 1
        }

        # Filter games to only include cities with multiple games
        filtered_games = [
            game for game in games
            if game['city'] in cities_with_multiple_games
        ]

        # Sort games by date
        sorted_games = sorted(filtered_games, key=lambda x: x['date'])

        if not sorted_games:
            return {}

        result = {}
        
        if weekdays:
            # Group by week ranges when weekdays are specified
            weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            weekday_range = f"{weekday_labels[weekdays[0]]}-{weekday_labels[weekdays[-1]]}"
            
            # Group games by week
            current_week = None
            current_week_games = []
            
            for game in sorted_games:
                game_date = datetime.strptime(game['date'], '%Y-%m-%d')
                week_start = game_date - timedelta(days=game_date.weekday() - weekdays[0])
                week_key = week_start.strftime('%Y-%m-%d')
                
                if week_key != current_week:
                    if current_week and current_week_games:
                        # Process previous week
                        week_end = datetime.strptime(current_week_games[-1]['date'], '%Y-%m-%d')
                        date_range = f"{weekday_range} ({current_week} - {week_end.strftime('%Y-%m-%d')})"
                        result[date_range] = self._organize_by_city(current_week_games)
                    
                    current_week = week_key
                    current_week_games = [game]
                else:
                    current_week_games.append(game)
            
            # Process the last week
            if current_week and current_week_games:
                week_end = datetime.strptime(current_week_games[-1]['date'], '%Y-%m-%d')
                date_range = f"{weekday_range} ({current_week} - {week_end.strftime('%Y-%m-%d')})"
                result[date_range] = self._organize_by_city(current_week_games)
        
        else:
            # Group by individual dates when no weekdays specified
            for date, games_in_date in groupby(sorted_games, key=itemgetter('date')):
                result[date] = self._organize_by_city(list(games_in_date))

        return result

    def _organize_by_city(self, games):
        """Helper method to organize games by city."""
        city_games = {}
        for game in sorted(games, key=lambda x: x['time']):
            if game['city'] not in city_games:
                city_games[game['city']] = []
            city_games[game['city']].append(game)
        return city_games