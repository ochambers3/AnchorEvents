import requests
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import os

class FetchData:
    #   Fetch NBA Schedule
    def fetch_nba_schedule(self):
        print("Fetching NBA Games")
        url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json"
        response = requests.get(url)
        return response.json()
    
    #  Fetch NHL Schedule by team.
    def fetch_nhl_schedule_by_team(self):
        print("Fetching NHL Games")
        teams = [
            "ANA", "ARI", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ", "DAL", 
            "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR", 
            "OTT", "PHI", "PIT", "SJS", "SEA", "STL", "TBL", "TOR", "VAN", "VGK", "WSH", "WPG"
        ]
        nhl_schedule = []
        for team in teams:
            url = f"https://api-web.nhle.com/v1/club-schedule-season/{team}/now"
            response = requests.get(url)
            nhl_schedule += response.json().get('games', [])
            # nhl_schedule += response.json()
        # print("Schedule: ", nhl_schedule)
        return nhl_schedule
    
    #  Fetch NHL Schedule by team.
    def fetch_nfl_schedule_by_team(self):
        print("Fetching NFL Games")
        teams = [
            "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", 
            "DET", "GB", "HOU", "IND", "JAX", "KC", "LV", "LAC", "LAR", "MIA", 
            "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SF", "SEA", "TB", 
            "TEN", "WAS"
        ]

        nfl_schedule = []
        for team in teams:
            url = f"http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team}/schedule?season=2025"
            response = requests.get(url)
            nfl_schedule += response.json().get('events', [])
        return nfl_schedule
    

    def fetch_ticketmaster_concerts(self, city, start_date, end_date, page=0):
        print(f"Fetching concerts in US, page {page}")
        api_key = os.environ.get('TICKETMASTER')
        print('using api key: ', api_key)
        base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "apikey": api_key,
            "classificationName": "music",
            "city": city,
            "countryCode": "US",  # or "CA" depending on city
            # "startDateTime": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "startDateTime": start_date,
            "endDateTime": end_date,
            "size": 1,
            "page": page
        }
        response = requests.get(base_url, params=params)
        print('found events: ', response.json())
        return response.json()