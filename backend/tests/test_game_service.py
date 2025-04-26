import pytest
from datetime import datetime
from service.game_service import GameService

class MockRepo:
    def get_games(self, db, start_date=None, end_date=None, cities=None, leagues=None):
        # Test data with multiple games in the same cities on different days
        return [
            # Chicago games (3 games)
            {"game_id": 1, "league": "NBA", "date": "2025-04-15", "time": "19:00", "team_away": "Lakers", "team_home": "Bulls", "venue": "United Center", "city": "Chicago"},
            {"game_id": 2, "league": "NHL", "date": "2025-04-15", "time": "20:00", "team_away": "Blackhawks", "team_home": "Red Wings", "venue": "United Center", "city": "Chicago"},
            {"game_id": 3, "league": "NBA", "date": "2025-04-17", "time": "19:30", "team_away": "Celtics", "team_home": "Bulls", "venue": "United Center", "city": "Chicago"},
            
            # New York games (2 games)
            {"game_id": 4, "league": "NBA", "date": "2025-04-16", "time": "19:00", "team_away": "Nets", "team_home": "Knicks", "venue": "Madison Square Garden", "city": "New York"},
            {"game_id": 5, "league": "NHL", "date": "2025-04-18", "time": "19:00", "team_away": "Rangers", "team_home": "Islanders", "venue": "MSG", "city": "New York"},
            
            # Boston game (single game, should be filtered out)
            {"game_id": 6, "league": "NBA", "date": "2025-04-19", "time": "20:00", "team_away": "76ers", "team_home": "Celtics", "venue": "TD Garden", "city": "Boston"},
        ]

@pytest.fixture
def service(monkeypatch):
    game_service = GameService()
    monkeypatch.setattr(game_service, "repository", MockRepo())
    return game_service

def test_weekday_filtering(service):
    """Test filtering games by weekdays."""
    # Monday (0) and Wednesday (2)
    data = {
        "weekdays": [0, 2]  # Monday and Wednesday
    }
    games = service.get_games(None, data)
    
    # Check that only games on Monday and Wednesday are included
    for date, cities in games.items():
        weekday = datetime.strptime(date, '%Y-%m-%d').weekday()
        assert weekday in [0, 2]

def test_multiple_cities_filtering(service):
    """Test filtering games by multiple cities."""
    data = {
        "cities": ["Chicago", "New York"]
    }
    games = service.get_games(None, data)
    
    # Check that only Chicago and New York games are included
    for date, cities in games.items():
        assert all(city in ["Chicago", "New York"] for city in cities.keys())

def test_cities_with_multiple_games(service):
    """Test that only cities with multiple games are included."""
    data = {}  # No filters
    games = service.get_games(None, data)
    
    # Boston should be filtered out as it only has one game
    for date, cities in games.items():
        assert "Boston" not in cities
        
    # Chicago and New York should be included as they have multiple games
    has_chicago = False
    has_new_york = False
    for date, cities in games.items():
        if "Chicago" in cities:
            has_chicago = True
        if "New York" in cities:
            has_new_york = True
    
    assert has_chicago and has_new_york

def test_weekday_and_city_filtering(service):
    """Test combining weekday and city filters."""
    # Tuesday (1) and Thursday (3)
    data = {
        "weekdays": [1, 3],  # Tuesday and Thursday
        "cities": ["Chicago", "New York"]
    }
    games = service.get_games(None, data)
    
    for date, cities in games.items():
        # Check weekday filter
        weekday = datetime.strptime(date, '%Y-%m-%d').weekday()
        assert weekday in [1, 3]
        
        # Check city filter
        assert all(city in ["Chicago", "New York"] for city in cities.keys())
