from datetime import timedelta, datetime

team_mapping = {
    "Anaheim": "Ducks",
    "Arizona": "Coyotes",
    "Boston": "Bruins",
    "Buffalo": "Sabres",
    "Calgary": "Flames",
    "Carolina": "Hurricanes",
    "Chicago": "Blackhawks",
    "Colorado": "Avalanche",
    "Columbus": "Blue Jackets",
    "Dallas": "Stars",
    "Detroit": "Red Wings",
    "Edmonton": "Oilers",
    "Florida": "Panthers",
    "Los Angeles": "Kings",
    "Minnesota": "Wild",
    "Montreal": "Canadiens",
    "Nashville": "Predators",
    "New Jersey": "Devils",
    "New York": "Rangers",
    "Ottawa": "Senators",
    "Philadelphia": "Flyers",
    "Pittsburgh": "Penguins",
    "San Jose": "Sharks",
    "Seattle": "Kraken",
    "St. Louis": "Blues",
    "Tampa Bay": "Lightning",
    "Toronto": "Maple Leafs",
    "Vancouver": "Canucks",
    "Vegas": "Golden Knights",
    "Washington": "Capitals",
    "Winnipeg": "Jets"
}

def get_team_name(city):
    return team_mapping.get(city, "Unknown")

def estimate_end_time(start_time, event_type, league=None):
    # Default durations (can be adjusted)
    durations = {
        'concert': timedelta(hours=2.5),
        'NBA': timedelta(hours=2.5),
        'NHL': timedelta(hours=2.5),
        'NFL': timedelta(hours=3),
        'MLB': timedelta(hours=3.5),
        'default_sport': timedelta(hours=2.5),
    }

    if event_type == 'concert':
        duration = durations['concert']
    elif event_type == 'sports':
        duration = durations.get(league, durations['default_sport'])
    else:
        duration = timedelta(hours=2)  # fallback

    end_time = start_time + duration
    return end_time