import requests
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import os
from dotenv import load_dotenv

load_dotenv()

class FetchData:
    #   Fetch NBA Schedule
    def fetch_nba_schedule(self):
        print("Fetching NBA Games")
        url = os.environ.get("NBA_URL")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    #  Fetch NHL Schedule by team.
    def fetch_nhl_schedule_by_team(self):
        print("Fetching NHL Games")
        teams = [
            "ANA", "ARI", "BOS", "BUF", "CGY", "CAR", "CHI", "COL", "CBJ", "DAL", 
            "DET", "EDM", "FLA", "LAK", "MIN", "MTL", "NSH", "NJD", "NYI", "NYR", 
            "OTT", "PHI", "PIT", "SJS", "SEA", "STL", "TBL", "TOR", "VAN", "VGK", "WSH", "WPG"
        ]
        url_template = os.environ.get('NHL_URL')
        nhl_schedule = []
        for team in teams:
            url = url_template.format(team=team)
            response = requests.get(url)
            response.raise_for_status()
            nhl_schedule += response.json().get('games', [])
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
        url_template = os.environ.get('NFL_URL')
        nfl_schedule = []
        for team in teams:
            url = url_template.format(team=team)
            response = requests.get(url)
            nfl_schedule += response.json().get('events', [])
        return nfl_schedule
    

    def fetch_ticketmaster_concerts(self, city, start_date, end_date, page=0):
        print(f"Fetching concerts in {city}, page {page}")
        api_key = os.environ.get('TICKETMASTER_API_KEY')
        base_url = os.environ.get('TICKETMASTER_URL')
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
        return response.json()