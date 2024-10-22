from api.nhl_api_client import NHLApiClient
from api.nba_api_client import NBAApiClient
from api.nfl_api_client import NFLApiClient
from repository.game_repository import GameRepository
from datetime import datetime, timedelta, date
from service.team_names import get_team_name

class GameService:

    def __init__(self, db):
        self.db = db
        self.nhl_api = NHLApiClient()
        self.nba_api = NBAApiClient()
        self.nfl_api = NFLApiClient()
        self.repository = GameRepository()

    def fetch_nhl_schedule(self):
        nhl_schedule = self.nhl_api.fetch_nhl_schedule_by_team()
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

    def fetch_nba_schedule(self):
        nba_schedule = self.nba_api.fetch_nba_schedule()
        nba_games = []
        for lscd_item in nba_schedule['lscd']:
            mscd = lscd_item['mscd']
            # month = mscd['mon']  # Extract the month
            games = mscd['g']    # List of games in that month

            for game in games:
                myGame = {}
                myGame['id'] = game["gid"]
                myGame['date'] = game["gdte"]
                #local time
                myGame['time'] = game['htm']
                myGame['awayTeam'] = game["v"]["tc"] + " " + game["v"]["tn"]
                myGame['homeTeam'] = game["h"]["tc"] + " " + game["h"]["tn"]
                myGame['venue'] = game["an"]
                myGame['city'] = game["ac"]
                nba_games.append(myGame)
            self.repository.save_schedule("NBA", nba_games, self.db)

    def fetch_nfl_schedule(self):
        nfl_schedule = self.nfl_api.fetch_nfl_schedule_by_team()
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

    def get_games(self, db, data):

        start_date = data.get("start_date", datetime.today().strftime('%Y-%m-%d'))
        end_date = data.get("end_date", None)
        city = data.get("city", None)
        weekend = data.get("weekend", None)
        # print("Start Date: ", start_date)
        # print(type(start_date))

        games = self.repository.get_games(db, start_date, end_date, city)
        for game in games:
            print(game)

        # If the weekend filter is applied, group by weekend
        if weekend == True:
            events = self.group_by_weekend(games)
            # for weekend in events:
            #     print(weekend)true
            #     for city in events[weekend]:
            #         print(" ", city)
            #         for event in events[weekend][city]:
            #             print(" ", event)
            events = self.get_min_games(events)
            # for weekend in events:
            #     print(weekend)
            #     for city in events[weekend]:
            #         print(" ", city)
            #         for event in events[weekend][city]:
            #             print(" ", event)
            return events
        games = self.format_response(games)
        return games
    
    def format_response(self, events):
        grouped_events = {}
        for event in events:
            game_id, league, date, time, team_away, team_home, venue, city = event
            if date not in grouped_events:
                grouped_events[date] = {}
            if city not in grouped_events[date]:
                grouped_events[date][city] = []

            grouped_events[date][city].append({
                "id": game_id,
                "date": date,
                "time": time,
                "team_away": team_away,
                "team_home": team_home,
                "venue": venue,
                "league": league
            })
        return grouped_events
    
    def group_by_weekend(self, events):
        # Group events by weekend
        grouped_events = {}
        for event in events:
            game_id, league, date, time, team_away, team_home, venue, city = event
            weekend_start = self.get_weekend_start(date)

            if weekend_start not in grouped_events:
                grouped_events[weekend_start] = {}
            if city not in grouped_events[weekend_start]:
                grouped_events[weekend_start][city] = []

            grouped_events[weekend_start][city].append({
                "id": game_id,
                "date": date,
                "time": time,
                "team_away": team_away,
                "team_home": team_home,
                "venue": venue,
                "league": league
            })
        return grouped_events
    
    def get_weekend_start(self, my_date):
        # Logic to calculate the weekend start (Friday)
        my_date = datetime.strptime(my_date, "%Y-%m-%d")
        week_day = date.weekday(my_date)
        if week_day == 4:
            return str(my_date)[:10]
        elif week_day == 5:  # Saturday
            return str(my_date - timedelta(days=1))[:10]
        elif week_day == 6:  # Sunday
            return str(my_date - timedelta(days=2))[:10]
        return str(my_date)[:10]  # Thursday or earlier
    
    def get_min_games(self, games):
        remove = False
        cities = []
        weekends = []
        for weekend in games:
            for city in games[weekend]:
                if len(games[weekend][city]) < 2:
                    cities.append(city)
            for city in cities:
                games[weekend].pop(city)
                cities = []
            if len(games[weekend]) == 0:
                weekends.append(weekend)
        for weekend in weekends:
            games.pop(weekend)
        return games

    
    def get_all_games(self, start_date, end_date):
        games = self.repository.get_all_games_in_range(start_date, end_date)
        return games
    
    def get_viscinity(self, block_length, min_events):
        games = self.repository.get_games_in_vicinity(block_length, min_events)
        return games
    
    def get_games_by_leagues(self, nfl_weight, nba_weight, nhl_weight, selected_leagues, start_date, end_date, db):
        games = self.repository.get_games_by_league(nfl_weight, nba_weight, nhl_weight, selected_leagues, start_date, end_date, db)
        return games

    # def get_games_by_league(self, league):

    # def get_games_by_team_and_league(self, league, team):



    