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
    
    
    def get_games_by_league(self, nfl_weight, nba_weight, nhl_weight, selected_leagues, start_date, end_date, db):
        query = """
            WITH WeekendBlocks AS (
                SELECT
                    city, 
                    date, 
                    time, 
                    team_away, 
                    team_home, 
                    venue, 
                    league,
                    CASE 
                        WHEN league = 'NFL' THEN ?
                        WHEN league = 'NBA' THEN ?
                        WHEN league = 'NHL' THEN ?
                        ELSE 0
                    END AS points,
                    CASE
                        WHEN strftime('%w', date) = '5' THEN date  -- Friday
                        WHEN strftime('%w', date) = '6' THEN date(date, '-1 day')  -- Saturday -> Friday
                        WHEN strftime('%w', date) = '0' THEN date(date, '-2 day')  -- Sunday -> Friday
                    END AS weekend_start
                FROM 
                    games
                WHERE 
                    league IN ({})
                    AND date BETWEEN ? AND ?
                    AND strftime('%w', date) IN ('5', '6', '0')
            )
            SELECT
                weekend_start,
                city,
                SUM(points) +
                CASE
                    WHEN COUNT(DISTINCT league) = 3 AND COUNT(DISTINCT date) >= 3 THEN 5
                    ELSE 0
                END AS total_points,
                GROUP_CONCAT(date || ' ' || time || ': ' || team_away || ' @ ' || team_home, '\n' ORDER BY date, time) AS events
            FROM 
                WeekendBlocks
            GROUP BY 
                weekend_start,
                city
            HAVING
                COUNT(*) > 1
                AND total_points > 2
            ORDER BY 
                total_points DESC, weekend_start;
            """.format(','.join('?' for _ in selected_leagues))
        cursor = db.cursor()
        cursor.execute(query, (nfl_weight, nba_weight, nhl_weight, *selected_leagues, start_date, end_date))
        games = cursor.fetchall()
        return games


    


    def get_games_in_vicinity(self, block_length, min_events):
        query = '''
            WITH EventGroups AS (
                SELECT
                    city,
                    date,
                    julianday(date) - julianday(LAG(date, 1) OVER (PARTITION BY city ORDER BY date)) AS days_since_last_event
                FROM games
            ),
            EventBlocks AS (
                SELECT
                    city,
                    date,
                    SUM(CASE 
                            WHEN days_since_last_event IS NULL OR days_since_last_event > ? THEN 1 
                            ELSE 0 
                        END) OVER (PARTITION BY city ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS block_id
                FROM EventGroups
            )
            SELECT
                city,
                COUNT(*) AS num_events,
                MIN(date) AS block_start,
                MAX(date) AS block_end
            FROM EventBlocks
            GROUP BY city, block_id
            HAVING COUNT(*) >= ?
            ORDER BY city, block_start
        '''

        # Corrected: fetching all the results from the query
        self.cursor.execute(query, (block_length, min_events))
        games = self.cursor.fetchall()  # Use fetchall() to get all matching rows
        return games
    










# def get_games_in_range(self, db, query_filters):
#         params = []
#         query = "SELECT city, date, time, team_away, team_home, venue, league"

#         if query_filters["weekend"] == "True":
#             query += (""",
#                     CASE
#                         WHEN strftime('%w', date) = '5' THEN date  -- Friday
#                         WHEN strftime('%w', date) = '6' THEN date(date, '-1 day')  -- Saturday -> Friday
#                         WHEN strftime('%w', date) = '0' THEN date(date, '-2 day')  -- Sunday -> Friday
#                     END AS weekend_start""")
        
#         query += (" FROM games WHERE 1=1")

#         if query_filters["start_date"]:
#             query += " AND date >= ?"
#             params.append(query_filters["start_date"])
            
            
#         if query_filters["end_date"]:
#             query += " AND date <= ?"
#             params.append(query_filters["end_date"])
        
#         if query_filters["city"]:
#             query += " AND city = ?"
#             params.append(query_filters["city"])

#         if query_filters["weekend"] == "True":
#             query += """ AND strftime('%w', date) IN ('5', '6', '0') 
#                     GROUP BY weekend_start, city 
#                     HAVING count(*) > 1 
#                     ORDER BY weekend_start, city"""
#         else:
#             query += " ORDER BY date, time;"

#         # handle weighting logic here if necessary
#         cursor = db.cursor()
#         print("Filters: ", query_filters)
#         print("Params: ", params)

#         # Execute the query with the dynamic parameters
#         result = cursor.execute(query, tuple(params)).fetchall()
    
#         # if leagues:
#         #     query += " AND league IN ({})".format(','.join(['?']*len(leagues)))
#         #     params.extend(leagues)

#         if query_filters.get("weekend") == "True":
#             grouped_results = {}
            
#             for row in result:
#                 city, date, time, team_away, team_home, venue, league, weekend_start = row
                
#                 # Grouping by weekend_start
#                 if weekend_start not in grouped_results:
#                     grouped_results[weekend_start] = {}

#                 # Grouping by city under weekend_start
#                 if city not in grouped_results[weekend_start]:
#                     grouped_results[weekend_start][city] = []

#                 # Append the event to the respective city under the weekend_start group
#                 grouped_results[weekend_start][city].append({
#                     "date": date,
#                     "time": time,
#                     "team_away": team_away,
#                     "team_home": team_home,
#                     "venue": venue,
#                     "league": league
#                 })

#             return grouped_results  # Return a nested dictionary with weekends and cities
        
#         return result  # Return plain data for non-weekend queries
    