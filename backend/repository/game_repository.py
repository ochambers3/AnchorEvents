import sqlite3

class GameRepository:
    def __init__(self):
        pass

    def save_schedule(self, league, schedule, db):
        cursor = db.cursor()
        for game in schedule:
            cursor.execute('''
                INSERT OR IGNORE INTO games (game_id, league, date, time, team_away, team_home, venue, city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game['id'], league, game['date'], game['time'], 
                  game['awayTeam'], 
                  game['homeTeam'], 
                  game['venue'], 
                  game['city']))
        db.commit()

    def get_games(self, db, start_date, end_date, city):
        query = "SELECT * FROM games WHERE 1=1"
        params = []

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if city:
            query += " AND city = ?"
            params.append(city)

        query += " ORDER BY date, time"
        cursor = db.cursor()
        return cursor.execute(query, tuple(params)).fetchall()