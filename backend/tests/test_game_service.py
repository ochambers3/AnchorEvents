import pytest
from datetime import datetime
from game_service import GameService

class MockRepo:
    def get_events(self, db, start_date=None, end_date=None, cities=None, leagues=None):
        """Mock repository that returns predictable test data and respects filters."""
        # Base test data
        all_events = [
            # Monday 2025-04-14 (weekday 0) - Chicago games
            {"id": 1, "event_id": "1", "type": "sports", "league": "NBA", "date": "2025-04-14", "start_time": "19:00", "end_time": "20:00", "artist": None, "team_away": "Lakers", "team_home": "Bulls", "venue": "United Center", "city": "Chicago"},
            {"id": 2, "event_id": "2", "type": "sports", "league": "NHL", "date": "2025-04-14", "start_time": "20:00", "end_time": "20:00", "artist": None, "team_away": "Blackhawks", "team_home": "Red Wings", "venue": "United Center", "city": "Chicago"},
            
            # Tuesday 2025-04-15 (weekday 1) - New York games
            {"id": 3, "event_id": "3", "type": "sports", "league": "NBA", "date": "2025-04-15", "start_time": "19:00", "end_time": "20:00", "artist": None, "team_away": "Nets", "team_home": "Knicks", "venue": "Madison Square Garden", "city": "New York"},
            {"id": 4, "event_id": "4", "type": "sports", "league": "NHL", "date": "2025-04-15", "start_time": "20:00", "end_time": "20:00", "artist": None, "team_away": "Rangers", "team_home": "Islanders", "venue": "MSG", "city": "New York"},
            
            # Wednesday 2025-04-16 (weekday 2) - Chicago game
            {"id": 5, "event_id": "5", "type": "sports", "league": "NBA", "date": "2025-04-16", "start_time": "19:30", "end_time": "20:00", "artist": None, "team_away": "Celtics", "team_home": "Bulls", "venue": "United Center", "city": "Chicago"},
            
            # Thursday 2025-04-17 (weekday 3) - New York game
            {"id": 6, "event_id": "6", "type": "sports", "league": "NHL", "date": "2025-04-17", "start_time": "19:00", "end_time": "20:00", "artist": None, "team_away": "Devils", "team_home": "Rangers", "venue": "MSG", "city": "New York"},
            
            # Friday 2025-04-18 (weekday 4) - Boston game (single game, should be filtered out)
            {"id": 7, "event_id": "7", "type": "sports", "league": "NBA", "date": "2025-04-18", "start_time": "20:00", "end_time": "20:00", "artist": None, "team_away": "76ers", "team_home": "Celtics", "venue": "TD Garden", "city": "Boston"},
            
            # Saturday 2025-04-19 (weekday 5) - Los Angeles games
            {"id": 8, "event_id": "8", "type": "sports", "league": "NBA", "date": "2025-04-19", "start_time": "20:30", "end_time": "20:00", "artist": None, "team_away": "Warriors", "team_home": "Lakers", "venue": "Crypto.com Arena", "city": "Los Angeles"},
            {"id": 9, "event_id": "9", "type": "sports", "league": "NHL", "date": "2025-04-19", "start_time": "19:00", "end_time": "20:00", "artist": None, "team_away": "Ducks", "team_home": "Kings", "venue": "Crypto.com Arena", "city": "Los Angeles"},
            
            # Sunday 2025-04-20 (weekday 6) - Los Angeles games
            {"id": 10, "event_id": "10", "type": "sports", "league": "NBA", "date": "2025-04-20", "start_time": "18:00", "end_time": "20:00", "artist": None, "team_away": "Clippers", "team_home": "Lakers", "venue": "Crypto.com Arena", "city": "Los Angeles"},
            {"id": 11, "event_id": "11", "type": "sports", "league": "NHL", "date": "2025-04-20", "start_time": "19:30", "end_time": "20:00", "artist": None, "team_away": "Sharks", "team_home": "Kings", "venue": "Crypto.com Arena", "city": "Los Angeles"},
            
            # Monday 2025-04-21 (weekday 0) - Los Angeles games (for wrap-around test)
            {"id": 12, "event_id": "12", "type": "sports", "league": "NBA", "date": "2025-04-21", "start_time": "19:00", "end_time": "20:00", "artist": None, "team_away": "Suns", "team_home": "Lakers", "venue": "Crypto.com Arena", "city": "Los Angeles"},
            {"id": 13, "event_id": "13", "type": "sports", "league": "NHL", "date": "2025-04-21", "start_time": "20:00", "end_time": "20:00", "artist": None, "team_away": "Golden Knights", "team_home": "Kings", "venue": "Crypto.com Arena", "city": "Los Angeles"},
            
            # Tuesday 2025-04-22 (weekday 1) - Los Angeles games (for wrap-around test)
            {"id": 14, "event_id": "14", "type": "sports", "league": "NBA", "date": "2025-04-22", "start_time": "19:30", "end_time": "20:00", "artist": None, "team_away": "Jazz", "team_home": "Lakers", "venue": "Crypto.com Arena", "city": "Los Angeles"},
            
            # A future week - Chicago games (for multiple week test)
            {"id": 15, "event_id": "15", "type": "sports", "league": "NBA", "date": "2025-04-28", "start_time": "19:00", "end_time": "20:00", "artist": None, "team_away": "Heat", "team_home": "Bulls", "venue": "United Center", "city": "Chicago"},
            {"id": 16, "event_id": "16", "type": "sports", "league": "NHL", "date": "2025-04-29", "start_time": "20:00", "end_time": "20:00", "artist": None, "team_away": "Lightning", "team_home": "Blackhawks", "venue": "United Center", "city": "Chicago"},
        ]
        
        # Apply filters just like the real repository would
        filtered_events = all_events
        
        # Filter by date range
        if start_date:
            filtered_events = [e for e in filtered_events if e['date'] >= start_date]
        if end_date:
            filtered_events = [e for e in filtered_events if e['date'] <= end_date]
        
        # Filter by cities
        if cities:
            filtered_events = [e for e in filtered_events if e['city'] in cities]
        
        # Filter by leagues
        if leagues:
            filtered_events = [e for e in filtered_events if e['league'] in leagues]
        
        return filtered_events

@pytest.fixture
def service(monkeypatch):
    """Create a GameService with mocked repository."""
    game_service = GameService()
    monkeypatch.setattr(game_service, "repository", MockRepo())
    return game_service


def test_empty_results_handling(service):
    """Test handling when no games match filters."""
    filters = {
        "weekdays": [5, 6],  # Saturday and Sunday
        "cities": ["Miami"],  # City not in our mock data
        "min_events": 2
    }
    result = service.get_events(None, filters)
    
    assert isinstance(result, dict), "Should return a dictionary"
    assert "itineraries" in result, "Should have itineraries key"
    assert len(result["itineraries"]) == 0, "Should return empty itineraries when no games match"


def test_basic_weekday_filtering(service):
    """Test basic weekday filtering without wrap-around."""
    filters = {
        "weekdays": [0, 1, 2],  # Monday, Tuesday, Wednesday
        "min_events": 2
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    
    # Should have itineraries for Chicago and New York
    assert len(itineraries) >= 2
    
    # Check that all events are on the correct weekdays
    for itinerary in itineraries:
        for event in itinerary["events"]:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            assert event_date.weekday() in [0, 1, 2]


def test_weekend_wrap_around(service):
    """Test weekend wrap-around functionality (Fri-Tue)."""
    filters = {
        "weekdays": [4, 5, 6, 0, 1],  # Friday through Tuesday
        "min_events": 2
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    
    # Should find Los Angeles itinerary that spans Fri-Tue
    la_itineraries = [it for it in itineraries if it["city"] == "Los Angeles"]
    assert len(la_itineraries) >= 1
    
    # Check that we have events spanning the weekend
    for itinerary in la_itineraries:
        weekdays_found = set()
        for event in itinerary["events"]:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            weekdays_found.add(event_date.weekday())
        
        # Should have events from the specified weekday range
        assert weekdays_found.issubset(set([4, 5, 6, 0, 1]))


def test_minimum_events_filter(service):
    """Test that minimum events filter works correctly."""
    filters = {
        "weekdays": [4],  # Just Friday - only one game in Boston
        "min_events": 2
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    # Should be empty because Boston only has 1 game on Friday
    assert len(result["itineraries"]) == 0


def test_city_filtering(service):
    """Test filtering by specific cities."""
    filters = {
        "cities": ["Chicago"],
        "min_events": 2
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    
    # Should only have Chicago itineraries
    for itinerary in itineraries:
        assert itinerary["city"] == "Chicago"


def test_league_filtering(service):
    """Test filtering by specific leagues."""
    filters = {
        "leagues": ["NBA"],
        "min_events": 1
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    
    # Should only have NBA events
    for itinerary in itineraries:
        for event in itinerary["events"]:
            assert event["league"] == "NBA"


def test_itinerary_structure(service):
    """Test that itinerary objects have the correct structure."""
    filters = {
        "weekdays": [0, 1],  # Monday, Tuesday
        "min_events": 2
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    assert len(itineraries) > 0
    
    # Check itinerary structure
    for itinerary in itineraries:
        # Required fields
        assert "id" in itinerary
        assert "city" in itinerary
        assert "total_days" in itinerary
        assert "date_range" in itinerary
        assert "events" in itinerary
        assert "event_count" in itinerary
        
        # Date range structure
        assert "start" in itinerary["date_range"]
        assert "end" in itinerary["date_range"]
        assert "formatted" in itinerary["date_range"]
        
        # Event structure
        for event in itinerary["events"]:
            assert "id" in event
            assert "event_id" in event
            assert "league" in event
            assert "artist" in event
            assert "team" in event
            assert "venue" in event
            assert "date" in event
            assert "start_time" in event
            assert "end_time"
            assert "day_of_week" in event
            assert "formatted_date" in event


def test_no_weekday_filtering(service):
    """Test behavior when no weekdays are specified."""
    filters = {
        "min_events": 2
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    
    # Should have itineraries from multiple cities
    cities = set(it["city"] for it in itineraries)
    assert len(cities) >= 2


def test_date_range_filtering(service):
    """Test filtering by date range."""
    filters = {
        "start_date": "2025-04-14",
        "end_date": "2025-04-16",
        "min_events": 1
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    
    # All events should be within the date range
    for itinerary in itineraries:
        for event in itinerary["events"]:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            start_date = datetime.strptime("2025-04-14", "%Y-%m-%d")
            end_date = datetime.strptime("2025-04-16", "%Y-%m-%d")
            assert start_date <= event_date <= end_date


def test_multiple_itineraries_same_city(service):
    """Test that multiple itineraries can be created for the same city."""
    filters = {
        "cities": ["Chicago"],
        "min_events": 1
    }
    result = service.get_events(None, filters)
    
    assert "itineraries" in result
    itineraries = result["itineraries"]
    
    chicago_itineraries = [it for it in itineraries if it["city"] == "Chicago"]
    # Should potentially have multiple Chicago itineraries from different weeks
    assert len(chicago_itineraries) >= 1