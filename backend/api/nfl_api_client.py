import requests

class NFLApiClient:
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