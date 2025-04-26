import pytest
from service.game_service import GameService

class MockRepo:
    def get_db_games(self, db, start_date, end_date, city, leagues):
        return [
            (1, "NBA", "2025-04-15", "19:00", "Lakers", "Warriors", "Staples Center", "Los Angeles"),
            (2, "NBA", "2025-04-16", "18:00", "Heat", "Celtics", "FTX Arena", "Miami"),
            (3, "NBA", "2025-04-19", "20:00", "Bulls", "Knicks", "United Center", "Chicago"),
            (4, "NBA", "2025-04-19", "21:00", "Nets", "Raptors", "Barclays Center", "Brooklyn"),
        ]

@pytest.fixture
def service(monkeypatch):
    db = None
    game_service = GameService(db)
    monkeypatch.setattr(game_service, "repository", MockRepo())
    return game_service

def test_get_games_no_weekend(service):
    data = {"weekend": False}
    games = service.get_games(data)
    assert "2025-04-15" in games
    assert "2025-04-16" in games
    assert isinstance(games["2025-04-15"], dict)

def test_grouped_data_structure(service):
    data = {"weekend": False}
    games = service.get_games(data)
    for date, cities in games.items():
        assert isinstance(cities, dict)
        for city, city_games in cities.items():
            for game in city_games:
                assert "id" in game
                assert "date" in game
                assert "league" in game
