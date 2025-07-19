from api.fetch_data import FetchData
from game_repository import GameRepository
from datetime import datetime, timedelta, date, timezone
from api.utils import get_team_name, estimate_end_time
from dateutil import parser
from dateutil.parser import isoparse

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
            start_time = dt + offset
            end = estimate_end_time(start_time, 'sports', 'NHL')
            end_time = end.time().strftime('%H:%M')
            myGame['start_time'] = start_time.isoformat()
            myGame['end_time'] = end_time
            myGame['artist'] = None
            myGame['awayTeam'] = game['awayTeam']['placeName']['default'] + " " + get_team_name(game['awayTeam']['placeName']['default'])
            myGame['homeTeam'] = game['homeTeam']['placeName']['default'] + " " + get_team_name(game['homeTeam']['placeName']['default'])
            myGame['venue'] = game['venue']['default']
            myGame['city'] = game['homeTeam']['placeName']['default']
            myGame['league'] = 'NHL'
            myGame['type'] = 'sports'
            nhl_games.append(myGame)
            # print(myGame)
        self.repository.save_schedule(nhl_games, self.db)

    def nba_filter(self):
        nba_schedule = self.data.fetch_nba_schedule()
        nba_games = []

        league_schedule = nba_schedule['leagueSchedule']
        game_dates = league_schedule['gameDates']
        
        for game_date_item in game_dates:
            games = game_date_item['games']  # List of games for this date
            
            for game in games:
                date_str = game["homeTeamTime"]
                date = parser.isoparse(date_str).date()
                # date = datetime.strptime(date_str, "%Y-%m-%d").date()
                start_time = isoparse(game["homeTeamTime"])
                end_time = estimate_end_time(start_time, 'sports', 'NBA')
                myGame = {}
                myGame['event_id'] = game["gameId"]
                myGame['type'] = 'sports'
                myGame['date'] = date.isoformat()
                myGame['start_time'] = start_time.time().strftime('%H:%M')
                myGame['end_time'] = end_time.time().strftime('%H:%M')
                myGame['artist'] = None
                # gmany other game time options
                myGame['time'] = game['homeTeamTime']
                myGame['awayTeam'] = game["awayTeam"]["teamCity"] + " " + game["awayTeam"]["teamName"]
                myGame['homeTeam'] = game["homeTeam"]["teamCity"] + " " + game["homeTeam"]["teamName"]
                myGame['venue'] = game["arenaName"]
                myGame['city'] = game["arenaCity"]
                myGame['league'] = 'NBA'
                myGame['type'] = 'sports'
                nba_games.append(myGame)
        
        self.repository.save_schedule(nba_games, self.db)

    def nfl_filter(self):
        nfl_schedule = self.data.fetch_nfl_schedule_by_team()
        nfl_games = []
        for game in nfl_schedule:
            myGame = {}
            myGame['event_id'] = game['id']
            # date = game['date'][:10]
            date_str = game['date'][:10]
            date = parser.isoparse(date_str).date()
            start_time = dt = datetime.strptime(game['date'], "%Y-%m-%dT%H:%MZ")
            end_time = estimate_end_time(start_time, 'sports', 'NFL')
            #my_date = datetime.strptime(date, "%Y-%m-%d")
            myGame['date'] = date.isoformat()
            myGame['artist'] = None
            # utc_time = game['startTimeUTC']
            # local_offset = game['venueUTCOffset']
            # #local time
            # dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
            # hours_offset = int(local_offset[:3])
            # seconds_offset = int(local_offset[4:])
            # offset = timedelta(hours=hours_offset, minutes=seconds_offset)
            # myGame['time'] = dt + offset
            myGame['start_time'] = start_time.time().strftime('%H:%M')
            myGame['end_time'] = end_time.time().strftime('%H:%M')
            if game['competitions'][0]['competitors'][0]['homeAway'] == "home":
                myGame['homeTeam'] = game['competitions'][0]['competitors'][0]['team']['displayName']
                myGame['awayTeam'] = game['competitions'][0]['competitors'][1]['team']['displayName']
            else:
                myGame['homeTeam'] = game['competitions'][0]['competitors'][1]['team']['displayName']
                myGame['awayTeam'] = game['competitions'][0]['competitors'][0]['team']['displayName']

            myGame['venue'] = game['competitions'][0]['venue']['fullName']
            myGame['city'] = game['competitions'][0]['venue']['address']['city']
            myGame['league'] = 'NFL'
            myGame['type'] = 'sports'
            nfl_games.append(myGame)
        self.repository.save_schedule(nfl_games, self.db)

    def ticketmaster_concert_filter(self, cities, pages = 1):
        print("Filtering Ticketmaster concerts")
        concerts = []
        start_date = datetime.now(timezone.utc)
        end_date = start_date + timedelta(days=180)
        formatted_start_date = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        formatted_end_date = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        for city in cities:
            page = 0
            while page < pages:
                data = self.data.fetch_ticketmaster_concerts(city, formatted_start_date, formatted_end_date, page)
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
                            try:
                                # Try with seconds
                                time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
                            except ValueError:
                                # Try without seconds
                                time_obj = datetime.strptime(time_str, "%H:%M").time()
                        else:
                            # Default to midnight if no time provided
                            time_obj = datetime.strptime("00:00:00", "%H:%M:%S").time()

                        start_time = datetime.combine(date_obj, time_obj)
                        # print("start_time: ", start_time, type(start_time))
                        # print("formatted ", start_time.strftime('%Y-%m-%d %H:%M'), type(start_time.strftime('%Y-%m-%d %H:%M')))

                        end_time = estimate_end_time(start_time, 'concert')
                        # end_time = datetime.strptime(end, '%m/%d/%y %H:%M:%S')
                        # print("end_time: ", end_time, type(end_time))

                        # print("iso format: ", start_time.time().strftime('%H:%M'), end_time.time().strftime('%H:%M'))
                        # print("date: ", date_obj.isoformat())
                        
                        # date_string = date_obj.isoformat()
                        # datetime_string = start_time.isoformat()
                        
                        concert = {
                            'event_id': e['id'],
                            'type': 'concert',
                            'league': None,
                            'artist': e['name'],
                            'date': date_obj.isoformat(),
                            'start_time': start_time.time().strftime('%H:%M'),
                            'end_time': end_time.time().strftime('%H:%M'),
                            'homeTeam': None,
                            'awayTeam': None,
                            'venue': e['_embedded']['venues'][0]['name'],
                            'city': e['_embedded']['venues'][0]['city']['name'],
                        }
                        concerts.append(concert)
                    except Exception as ex:
                        print("Skipping event due to error:", ex)

                if "page" not in data or data["page"]["number"] >= data["page"]["totalPages"] - 1:
                    break
                page += 1

        self.repository.save_schedule(concerts, self.db)