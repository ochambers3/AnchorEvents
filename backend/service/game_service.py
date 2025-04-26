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
                - city: Optional city name
                - weekend: Optional boolean for weekend games only
        
        Returns:
            Dictionary of games organized by date and city
        """
        # Extract filter parameters
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')
        city = filters.get('city')
        weekend = filters.get('weekend', False)

        # Get games from repository
        games = self.repository.get_games(
            db,
            start_date=start_date,
            end_date=end_date,
            cities=[city] if city else None,
            leagues=None  # Currently not filtering by league
        )

        # Organize games by date and city
        organized_games = {}
        for game in games:
            date = game['date']
            city = game['city']
            
            # Create date entry if it doesn't exist
            if date not in organized_games:
                organized_games[date] = {}
            
            # Create city entry if it doesn't exist
            if city not in organized_games[date]:
                organized_games[date][city] = []
            
            # Add game to the appropriate date and city
            game_dict = {
                'id': game['game_id'],
                'league': game['league'],
                'date': game['date'],
                'time': game['time'],
                'team_away': game['team_away'],
                'team_home': game['team_home'],
                'venue': game['venue']
            }
            organized_games[date][city].append(game_dict)

        return organized_games