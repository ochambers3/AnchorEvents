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

    def format_date(self, start_date, end_date):
        """
        Takes two dates in 'YYYY-MM-DD' format and returns relevant format.

        # January 8 - 10, 2024
        # January 8 - February 10, 2024
        # December 8, 2024 - January 10, 2025
        """
        date_string = ""

        # Parse each date ONCE
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        start_year = start.year
        start_month = start.strftime('%B')  # Full month name like "January"
        start_day = start.day

        end_year = end.year
        end_month = end.strftime('%B')      # Full month name like "February"
        end_day = end.day

        # Logic
        if start_year == end_year and start_month == end_month:
            date_string = f"{start_month} {start_day} - {end_day}, {start_year}"
        elif start_year == end_year and start_month != end_month:
            date_string = f"{start_month} {start_day} - {end_month} {end_day}, {end_year}"
        else:  # Different years
            date_string = f"{start_month} {start_day}, {start_year} - {end_month} {end_day}, {end_year}"

        return date_string

    def format_single_date(self, date):
        #make date a datetime object
        date = datetime.strptime(date, '%Y-%m-%d')
        return date.strftime('%b %d, %Y')

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
        min_games = filters.get('min_games', 1)
        min_games = int(min_games)

        # Get games from repository
        games = self.repository.get_games(
            db,
            start_date=start_date,
            end_date=end_date,
            cities=cities if cities else None
        )

        if weekdays:
            games = [
                game for game in games
                if datetime.strptime(game['date'], '%Y-%m-%d').weekday() in weekdays
            ]

        # Sort games by date first
        sorted_games = sorted(games, key=lambda x: x['date'])

        if not sorted_games:
            return {}

        result = {}
        
        if weekdays:
            # Group by week ranges when weekdays are specified
            weekday_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            weekday_range = f"{weekday_labels[weekdays[0]]}-{weekday_labels[weekdays[-1]]}"
            
            # Group games by week
            current_week = None
            week_games = []
            
            for game in sorted_games:
                game_date = datetime.strptime(game['date'], '%Y-%m-%d')
                # Calculate the start of the week containing the selected weekdays
                week_start = game_date - timedelta(days=game_date.weekday() - weekdays[0])
                
                if current_week != week_start:
                    # Process previous week's games if we have any
                    if week_games:
                        # Count games per city for this week
                        city_games = {}
                        for g in week_games:
                            city = g['city']
                            if city not in city_games:
                                city_games[city] = []
                            city_games[city].append(g)
                        
                        # Filter cities that meet minimum games requirement for this week
                        cities_with_enough_games = {
                            city for city, games_list in city_games.items()
                            if len(games_list) >= min_games
                        }
                        
                        # Only include games from cities that meet the requirement
                        filtered_week_games = [
                            g for g in week_games
                            if g['city'] in cities_with_enough_games
                        ]
                        
                        if filtered_week_games:
                            # Use current_week for the date range since we're processing the previous week
                            start_date = current_week.strftime('%Y-%m-%d')
                            end_date = (current_week + timedelta(days=len(weekdays)-1)).strftime('%Y-%m-%d')
                            # start = self.format_date(start_date)
                            # end = self.format_date(end_date)
                            # week_key = f"{start} - {end}"
                            week_key = self.format_date(start_date, end_date)
                            result[week_key] = self._organize_by_city(filtered_week_games)
                    
                    # Start new week
                    current_week = week_start
                    week_games = [game]
                else:
                    week_games.append(game)
            
            # Process the last week
            if week_games:
                city_games = {}
                for g in week_games:
                    city = g['city']
                    if city not in city_games:
                        city_games[city] = []
                    city_games[city].append(g)
                
                cities_with_enough_games = {
                    city for city, games_list in city_games.items()
                    if len(games_list) >= min_games
                }
                
                filtered_week_games = [
                    g for g in week_games
                    if g['city'] in cities_with_enough_games
                ]
                
                if filtered_week_games:
                    # Use current_week for the last week as well
                    start_date = current_week.strftime('%Y-%m-%d')
                    end_date = (current_week + timedelta(days=len(weekdays)-1)).strftime('%Y-%m-%d')
                    # start = self.format_date(start_date)
                    # end = self.format_date(end_date)
                    # week_key = f"{start} - {end}"
                    week_key = self.format_date(start_date, end_date)
                    result[week_key] = self._organize_by_city(filtered_week_games)
        
        else:
            # Group by individual dates when no weekdays specified
            for date, games_in_date in groupby(sorted_games, key=itemgetter('date')):
                result[date] = self._organize_by_city(list(games_in_date))

        print(result)

        return result

    def _organize_by_city(self, games):
        """Helper method to organize games by city."""
        city_games = {}
        for game in sorted(games, key=lambda x: x['time']):
            if game['city'] not in city_games:
                city_games[game['city']] = []
            city_games[game['city']].append(game)
        return city_games

#I am sorting by date which puts April first,
#I need to sort by date and then edit all dates to be what I want.