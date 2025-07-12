import pytest
from game_repository import GameRepository

@pytest.fixture
def sample_games():
    return [
        {
            'id': 1,
            'date': '2025-04-13',
            'time': '19:00',
            'artist': None,
            'awayTeam': 'Sharks',
            'homeTeam': 'Jets',
            'venue': 'Main Arena',
            'city': 'San Jose'
        },
        {
            'id': 2,
            'date': '2025-04-13',
            'time': '20:00',
            'artist': None,
            'awayTeam': 'Warriors',
            'homeTeam': 'Lakers',
            'venue': 'Chase Center',
            'city': 'San Francisco'
        },
        {
            'id': 3,
            'date': '2025-04-14',
            'time': '19:30',
            'artist': None,
            'awayTeam': 'Canucks',
            'homeTeam': 'Sharks',
            'venue': 'Main Arena',
            'city': 'San Jose'
        }
    ]

def test_save_schedule(app, db, sample_games):
    """Test saving games to the database."""
    with app.app_context():
        repo = GameRepository()

        cursor = db.cursor()
        cursor.execute('DELETE FROM events')
        db.commit()
        
        repo.save_schedule('NHL', sample_games, db)
        
        saved_games = cursor.execute('SELECT * FROM events').fetchall()
        assert len(saved_games) == len(sample_games)
        
        # Verify the data is correct
        for game in saved_games:
            assert game['league'] == 'NHL'
            assert game['city'] in ['San Jose', 'San Francisco']