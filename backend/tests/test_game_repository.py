import sqlite3
import pytest
from repository.game_repository import GameRepository
from datetime import datetime

@pytest.fixture
def mock_db():
    # Create in-memory SQLite DB
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row

    db.execute('''
        CREATE TABLE games (
            game_id TEXT PRIMARY KEY,
            league TEXT,
            date TEXT,
            time TEXT,
            team_away TEXT,
            team_home TEXT,
            venue TEXT,
            city TEXT
        )
    ''')
    db.commit()
    yield db
    db.close()

@pytest.fixture
def sample_games():
    return [
        {
            'id': 'nhl_1',
            'date': '2025-04-13',
            'time': '19:00',
            'awayTeam': 'Sharks',
            'homeTeam': 'Jets',
            'venue': 'Main Arena',
            'city': 'San Jose'
        },
        {
            'id': 'nba_1',
            'date': '2025-04-13',
            'time': '20:00',
            'awayTeam': 'Warriors',
            'homeTeam': 'Lakers',
            'venue': 'Chase Center',
            'city': 'San Francisco'
        },
        {
            'id': 'nhl_2',
            'date': '2025-04-14',
            'time': '19:30',
            'awayTeam': 'Canucks',
            'homeTeam': 'Sharks',
            'venue': 'Main Arena',
            'city': 'San Jose'
        }
    ]

def test_save_schedule(mock_db, sample_games):
    repo = GameRepository()
    
    # Save NHL games
    nhl_games = [g for g in sample_games if g['id'].startswith('nhl')]
    repo.save_schedule('NHL', nhl_games, mock_db)
    
    # Save NBA games
    nba_games = [g for g in sample_games if g['id'].startswith('nba')]
    repo.save_schedule('NBA', nba_games, mock_db)

    # Verify all games were saved
    cursor = mock_db.cursor()
    saved_games = cursor.execute('SELECT * FROM games ORDER BY date, time').fetchall()
    assert len(saved_games) == len(sample_games)

def test_get_games_filtering(mock_db, sample_games):
    repo = GameRepository()
    
    # Save all games
    for league, games in [
        ('NHL', [g for g in sample_games if g['id'].startswith('nhl')]),
        ('NBA', [g for g in sample_games if g['id'].startswith('nba')])
    ]:
        repo.save_schedule(league, games, mock_db)

    # Test date filtering
    results = repo.get_games(mock_db, start_date='2025-04-14')
    assert len(results) == 1
    assert results[0]['game_id'] == 'nhl_2'

    # Test city filtering
    results = repo.get_games(mock_db, cities=['San Jose'])
    assert len(results) == 2
    assert all(r['city'] == 'San Jose' for r in results)

    # Test league filtering
    results = repo.get_games(mock_db, leagues=['NHL'])
    assert len(results) == 2
    assert all(r['league'] == 'NHL' for r in results)

    # Test combined filters
    results = repo.get_games(
        mock_db,
        start_date='2025-04-13',
        end_date='2025-04-13',
        cities=['San Francisco'],
        leagues=['NBA']
    )
    assert len(results) == 1
    assert results[0]['game_id'] == 'nba_1'
