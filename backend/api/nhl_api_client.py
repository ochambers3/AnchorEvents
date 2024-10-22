import requests

class NHLApiClient:
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