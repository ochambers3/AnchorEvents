from repository.game_repository import GameRepository
from datetime import datetime, timedelta, date

class GameService:

    def __init__(self, db):
        self.db = db
        self.repository = GameRepository()

    def get_games(self, db, data):
        #Set variables if not in data. Start date is at least today's date
        start_date = data.get("start_date", datetime.today().strftime('%Y-%m-%d'))
        end_date = data.get("end_date", None)
        city = data.get("city", None)
        weekend = data.get("weekend", None)
        leagues = data.get("leagues", None)

        #Get data from the repository layer
        games = self.repository.get_games(db, start_date, end_date, city, leagues)


        # If the weekend filter is applied, group by weekend
        games = self.format_response(games, weekend)


        if weekend == True:
            # events = self.group_by_weekend(games)
            # events = self.get_min_games(events)
            games = self.get_min_games(games)
            # return events
        # games = self.format_response(games)
        return games
    
    def format_response(self, events, weekend):
        grouped_events = {}
        #For all events
        for event in events:
            game_id, league, date, time, team_away, team_home, venue, city = event

            if weekend == True:
                event_date = self.get_weekend_start(date)
            else:
                event_date = date
            # Group events by date
            if event_date not in grouped_events:
                grouped_events[event_date] = {}
            #Group events by city within event_date.
            if city not in grouped_events[event_date]:
                grouped_events[event_date][city] = []

            grouped_events[event_date][city].append({
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
        #Only return weekends with at least two games
        remove = False
        cities = []
        weekends = []
        for weekend in games:
            for city in games[weekend]:
                #Make a list of all cities with less than two events
                if len(games[weekend][city]) < 2:
                    cities.append(city)
            #remove those cities from the weekend
            for city in cities:
                games[weekend].pop(city)
            cities = []
            #Make a list of all weekends with no events
            if len(games[weekend]) == 0:
                weekends.append(weekend)
        #remove empty weekends from data
        for weekend in weekends:
            games.pop(weekend)
        return games
    



    