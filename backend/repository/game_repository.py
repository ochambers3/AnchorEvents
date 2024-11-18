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

    def get_games(self, db, start_date, end_date, city, leagues):
        query = "SELECT * FROM games WHERE 1=1"
        params = []

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
            
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        if city:
            query += " AND city IN ("
            for count, val in enumerate(city):
                if count+1 < len(city):
                    query += "?, "
                    params.append(val)
                else:
                    query += "?)"
                    params.append(val)

        if leagues:
            query += " AND league IN ("
            for count, val in enumerate(leagues):
                if count+1 < len(leagues):
                    query += "?, "
                    params.append(val)
                else:
                    query += "?)"
                    params.append(val)
                #params.append(val)


        query += " ORDER BY date, time"
        #return query, tuple(params)
        cursor = db.cursor()
        return cursor.execute(query, tuple(params)).fetchall()