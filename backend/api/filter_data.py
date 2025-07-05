from api.fetch_data import FetchData
from game_repository import GameRepository
from datetime import datetime, timedelta, date
from api.team_names import get_team_name

class FilterData:
    def __init__(self, db):
        self.db = db
        self.data = FetchData()
        self.repository = GameRepository()

    def nhl_filter(self):
        nhl_schedule = self.data.fetch_nhl_schedule_by_team()
        nhl_games = []
        for game in nhl_schedule:
            myGame = {}
            myGame['id'] = game['id']
            myGame['date'] = game['gameDate']
            utc_time = game['startTimeUTC']
            local_offset = game['venueUTCOffset']
            #local time
            dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
            hours_offset = int(local_offset[:3])
            seconds_offset = int(local_offset[4:])
            offset = timedelta(hours=hours_offset, minutes=seconds_offset)
            myGame['time'] = dt + offset
            myGame['awayTeam'] = game['awayTeam']['placeName']['default'] + " " + get_team_name(game['awayTeam']['placeName']['default'])
            myGame['homeTeam'] = game['homeTeam']['placeName']['default'] + " " + get_team_name(game['homeTeam']['placeName']['default'])
            myGame['venue'] = game['venue']['default']
            myGame['city'] = game['homeTeam']['placeName']['default']
            nhl_games.append(myGame)
            # print(myGame)
        self.repository.save_schedule("NHL", nhl_games, self.db)

    def nba_filter(self):
        nba_schedule = self.data.fetch_nba_schedule()
        nba_games = []

        league_schedule = nba_schedule['leagueSchedule']
        game_dates = league_schedule['gameDates']
        
        for game_date_item in game_dates:
            games = game_date_item['games']  # List of games for this date
            
            for game in games:
                myGame = {}
                myGame['id'] = game["gameId"]
                myGame['date'] = game["gameDateEst"][:10]
                # gmany other game time options
                myGame['time'] = game['homeTeamTime']
                myGame['awayTeam'] = game["awayTeam"]["teamCity"] + " " + game["awayTeam"]["teamName"]
                myGame['homeTeam'] = game["homeTeam"]["teamCity"] + " " + game["homeTeam"]["teamName"]
                myGame['venue'] = game["arenaName"]
                myGame['city'] = game["arenaCity"]
                nba_games.append(myGame)
        
        self.repository.save_schedule("NBA", nba_games, self.db)

    def nfl_filter(self):
        nfl_schedule = self.data.fetch_nfl_schedule_by_team()
        nfl_games = []
        for game in nfl_schedule:
            myGame = {}
            myGame['id'] = game['id']
            date = game['date'][:10]
            #my_date = datetime.strptime(date, "%Y-%m-%d")
            myGame['date'] = date
            # utc_time = game['startTimeUTC']
            # local_offset = game['venueUTCOffset']
            # #local time
            # dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
            # hours_offset = int(local_offset[:3])
            # seconds_offset = int(local_offset[4:])
            # offset = timedelta(hours=hours_offset, minutes=seconds_offset)
            # myGame['time'] = dt + offset
            myGame['time'] = game['date']
            if game['competitions'][0]['competitors'][0]['homeAway'] == "home":
                myGame['homeTeam'] = game['competitions'][0]['competitors'][0]['team']['displayName']
                myGame['awayTeam'] = game['competitions'][0]['competitors'][1]['team']['displayName']
            else:
                myGame['homeTeam'] = game['competitions'][0]['competitors'][1]['team']['displayName']
                myGame['awayTeam'] = game['competitions'][0]['competitors'][0]['team']['displayName']

            myGame['venue'] = game['competitions'][0]['venue']['fullName']
            myGame['city'] = game['competitions'][0]['venue']['address']['city']
            nfl_games.append(myGame)
        self.repository.save_schedule("NFL", nfl_games, self.db)