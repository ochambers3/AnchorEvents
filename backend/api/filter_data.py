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
            myGame['event_id'] = game['id']
            myGame['date'] = game['gameDate']
            utc_time = game['startTimeUTC']
            local_offset = game['venueUTCOffset']
            #local time
            dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
            hours_offset = int(local_offset[:3])
            seconds_offset = int(local_offset[4:])
            offset = timedelta(hours=hours_offset, minutes=seconds_offset)
            myGame['time'] = dt + offset
            myGame['artist'] = None
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
                myGame['event_id'] = game["gameId"]
                myGame['date'] = game["gameDateEst"][:10]
                myGame['artist'] = None
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
            myGame['event_id'] = game['id']
            date = game['date'][:10]
            #my_date = datetime.strptime(date, "%Y-%m-%d")
            myGame['date'] = date
            myGame['artist'] = None
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

    def ticketmaster_concert_filter(self, cities):
        print("Filtering Ticketmaster concerts")
        concerts = []
        start_date = datetime.now()
        end_date = start_date + timedelta(days=180)

        for city in cities:
            page = 0
            while True:
                data = self.data.fetch_ticketmaster_concerts(city, start_date, end_date, page)
                events = data.get('_embedded', {}).get('events', [])
                if not events:
                    break

                for e in events:
                    try:
                        date_str = e['dates']['start']['localDate']
                        time_str = e['dates']['start'].get('localTime')
                        
                        # Create a consistent datetime object
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                        
                        if time_str:
                            # Try different time formats
                            try:
                                # Try with seconds first
                                time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
                            except ValueError:
                                # Try without seconds
                                time_obj = datetime.strptime(time_str, "%H:%M").time()
                        else:
                            # Default to midnight if no time provided
                            time_obj = datetime.strptime("00:00:00", "%H:%M:%S").time()
                        
                        # Combine date and time into a single datetime object
                        datetime_obj = datetime.combine(date_obj, time_obj)
                        
                        # IMPORTANT: Convert to strings for database storage
                        date_string = date_obj.isoformat()  # "2025-11-20"
                        datetime_string = datetime_obj.isoformat()  # "2025-11-20T19:30:00"
                        
                        print("DATE: ", date_obj.isoformat())
                        print("TIME: ", datetime_obj.isoformat())
                        print(type(date_obj.isoformat()), type(datetime_obj.isoformat()))
                        
                        concert = {
                            'event_id': e['id'],
                            'artist': e['name'],
                            'date': date_str,  # Convert to string
                            'time': datetime_string,  # Convert to string
                            'homeTeam': None,
                            'awayTeam': None,
                            'venue': e['_embedded']['venues'][0]['name'],
                            'city': e['_embedded']['venues'][0]['city']['name'],
                        }
                        print('Concert: ', concert)
                        for item in concert:
                            print(item, type(item))
                        concerts.append(concert)
                    except Exception as ex:
                        print("Skipping event due to error:", ex)

                if "page" not in data or data["page"]["number"] >= data["page"]["totalPages"] - 1:
                    break
                page += 1

        self.repository.save_schedule("Concert", concerts, self.db)