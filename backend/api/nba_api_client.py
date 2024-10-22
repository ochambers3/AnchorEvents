import requests

class NBAApiClient:
    #  Fetch NBA Schedule
    def fetch_nba_schedule(self):
        url = "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2024/league/00_full_schedule.json"
        response = requests.get(url)
        return response.json()