import pytest
from datetime import datetime
from game_service import GameService

class MockRepo:
    def get_events(self, db, start_date=None, end_date=None, cities=None, leagues=None):
        """Mock repository that returns predictable test data."""
        # Using specific dates so weekday tests are predictable
        return [
            # Monday 2025-04-14 (weekday 0) - Chicago games
            {"game_id": 1, "league": "NBA", "date": "2025-04-14", "time": "19:00", "team_away": "Lakers", "team_home": "Bulls", "venue": "United Center", "city": "Chicago"},
            {"game_id": 2, "league": "NHL", "date": "2025-04-14", "time": "20:00", "team_away": "Blackhawks", "team_home": "Red Wings", "venue": "United Center", "city": "Chicago"},
            
            # Tuesday 2025-04-15 (weekday 1) - New York games
            {"game_id": 3, "league": "NBA", "date": "2025-04-15", "time": "19:00", "team_away": "Nets", "team_home": "Knicks", "venue": "Madison Square Garden", "city": "New York"},
            {"game_id": 4, "league": "NHL", "date": "2025-04-15", "time": "20:00", "team_away": "Rangers", "team_home": "Islanders", "venue": "MSG", "city": "New York"},
            
            # Wednesday 2025-04-16 (weekday 2) - Chicago game
            {"game_id": 5, "league": "NBA", "date": "2025-04-16", "time": "19:30", "team_away": "Celtics", "team_home": "Bulls", "venue": "United Center", "city": "Chicago"},
            
            # Thursday 2025-04-17 (weekday 3) - New York game
            {"game_id": 6, "league": "NHL", "date": "2025-04-17", "time": "19:00", "team_away": "Devils", "team_home": "Rangers", "venue": "MSG", "city": "New York"},
            
            # Friday 2025-04-18 (weekday 4) - Boston game (single game, should be filtered out)
            {"game_id": 7, "league": "NBA", "date": "2025-04-18", "time": "20:00", "team_away": "76ers", "team_home": "Celtics", "venue": "TD Garden", "city": "Boston"},
        ]

@pytest.fixture
def service(monkeypatch):
    """Create a GameService with mocked repository."""
    game_service = GameService()
    monkeypatch.setattr(game_service, "repository", MockRepo())
    return game_service

def test_weekday_filtering(service):
    """Test filtering games by weekdays."""
    # Test Monday (0) and Wednesday (2)
    data = {
        "weekdays": [0, 2]  # Monday and Wednesday
    }
    games = service.get_events(None, data)
    
    # Verify we got results
    assert len(games) > 0, "Should have games for Monday and Wednesday"
    
    # Check that only games on Monday and Wednesday are included
    for date, cities in games.items():
        weekday = datetime.strptime(date, '%Y-%m-%d').weekday()
        assert weekday in [0, 2], f"Game on {date} (weekday {weekday}) should not be included"

def test_multiple_cities_filtering(service):
    """Test filtering games by multiple cities."""
    data = {
        "cities": ["Chicago", "New York"]
    }
    games = service.get_events(None, data)
    
    # Verify we got results
    assert len(games) > 0, "Should have games for Chicago and New York"
    
    # Check that only Chicago and New York games are included
    for date, cities in games.items():
        for city in cities.keys():
            assert city in ["Chicago", "New York"], f"City {city} should not be included"

def test_cities_with_multiple_games(service):
    """Test that only cities with multiple games are included."""
    data = {}  # No filters
    games = service.get_events(None, data)
    
    # Verify we got results
    assert len(games) > 0, "Should have games when no filters applied"
    
    # Boston should be filtered out as it only has one game
    all_cities = set()
    for date, cities in games.items():
        all_cities.update(cities.keys())
    
    assert "Boston" not in all_cities, "Boston should be filtered out (only has one game)"
    assert "Chicago" in all_cities, "Chicago should be included (has multiple games)"
    assert "New York" in all_cities, "New York should be included (has multiple games)"

def test_weekday_and_city_filtering(service):
    """Test combining weekday and city filters."""
    # Tuesday (1) and Thursday (3)
    data = {
        "weekdays": [1, 3],  # Tuesday and Thursday
        "cities": ["Chicago", "New York"]
    }
    games = service.get_events(None, data)
    
    # We should get results (Tuesday has New York games, Thursday has New York games)
    assert len(games) > 0, "Should have games for Tuesday/Thursday in Chicago/New York"
    
    for date, cities in games.items():
        # Check weekday filter
        weekday = datetime.strptime(date, '%Y-%m-%d').weekday()
        assert weekday in [1, 3], f"Game on {date} (weekday {weekday}) should not be included"
        
        # Check city filter
        for city in cities.keys():
            assert city in ["Chicago", "New York"], f"City {city} should not be included"

def test_empty_results_handling(service):
    """Test handling when no games match filters."""
    data = {
        "weekdays": [5, 6],  # Saturday and Sunday (no games in our mock data)
        "cities": ["Chicago"]
    }
    games = service.get_events(None, data)
    
    # Should return empty dict, not crash
    assert isinstance(games, dict), "Should return a dictionary"
    assert len(games) == 0, "Should return empty results when no games match"