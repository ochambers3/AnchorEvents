import requests

class FetchData:
    #   Fetch NBA Schedule
    def fetch_nba_schedule(self):
        url = "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/2024/league/00_full_schedule.json"
        response = requests.get(url)
        return response.json()
    
    #  Fetch NHL Schedule by team.
    def fetch_nhl_schedule_by_team(self):
        print("Inside fetch nhl schedule by team")
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
        teams = [
            "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE", "DAL", "DEN", 
            "DET", "GB", "HOU", "IND", "JAX", "KC", "LV", "LAC", "LAR", "MIA", 
            "MIN", "NE", "NO", "NYG", "NYJ", "PHI", "PIT", "SF", "SEA", "TB", 
            "TEN", "WAS"
        ]

        nfl_schedule = []
        for team in teams:
            url = f"http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team}/schedule?season=2024"
            response = requests.get(url)
            nfl_schedule += response.json().get('events', [])
        return nfl_schedule