
from repository.game_repository import GameRepository

class GameTests:
    def __init__(self, db):
        self.db = db
        self.repository = GameRepository()

    def test_game_repository(self, db):
        query = self.repository.get_games(db, None, None, ['Toronto', 'Chicago', 'Winnipeg'], ['NFL', 'NHL'])
        print(query)
