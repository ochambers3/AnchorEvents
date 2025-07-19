import sqlite3
from typing import List, Dict, Any, Optional

class GameRepository:
    def save_schedule(self, league: str, schedule: List[Dict[str, Any]], db: sqlite3.Connection) -> None:
        """Save a list of events for a specific league to the database.
        
        Args:
            league: The sports league identifier (e.g., 'NHL', 'NBA')
            schedule: List of game dictionaries containing game details
            db: SQLite database connection
        """
        cursor = db.cursor()
        for game in schedule:
            cursor.execute('''
                INSERT OR IGNORE INTO events (event_id, league, "date", "time", artist, team_away, team_home, venue, city)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game['event_id'], league, game['date'], game['time'], game['artist'],
                  game['awayTeam'], 
                  game['homeTeam'], 
                  game['venue'], 
                  game['city']))
        db.commit()

    def get_events(self, db: sqlite3.Connection, 
                 start_date: Optional[str] = None, 
                 end_date: Optional[str] = None, 
                 cities: Optional[List[str]] = None, 
                 leagues: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Retrieve events from the database based on specified filters.
        
        Args:
            db: SQLite database connection
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)
            cities: Optional list of cities to filter by
            leagues: Optional list of leagues to filter by
            
        Returns:
            List of game records matching the specified criteria
        """
        query_parts = ["SELECT * FROM events WHERE 1=1"]
        params = []

        if start_date:
            query_parts.append("date >= ?")
            params.append(start_date)
            
        if end_date:
            query_parts.append("date <= ?")
            params.append(end_date)
        
        if cities:
            query_parts.append(f"city IN ({','.join('?' * len(cities))})")
            params.extend(cities)

        if leagues:
            query_parts.append(f"league IN ({','.join('?' * len(leagues))})")
            params.extend(leagues)

        query = " AND ".join(query_parts) + " ORDER BY date, time"
        
        cursor = db.cursor()
        cursor.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
        rows = cursor.execute(query, tuple(params)).fetchall()
        
        # Convert SQLite Row objects to dictionaries
        return [{
            'event_id': row['event_id'],
            'league': row['league'],
            'date': row['date'],
            'time': row['time'],
            'artist': row['artist'],
            'team_away': row['team_away'],
            'team_home': row['team_home'],
            'venue': row['venue'],
            'city': row['city']
        } for row in rows]