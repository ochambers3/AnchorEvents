from datetime import datetime, timedelta
from game_repository import GameRepository
from itertools import groupby
from operator import itemgetter
import uuid


class GameService:
    """Service layer for game-related operations."""

    def __init__(self):
        """Initialize the game service."""
        self.repository = GameRepository()

    def format_date(self, start_date, end_date):
        """
        Takes two dates in 'YYYY-MM-DD' format and returns relevant format.

        # January 8 - 10, 2024
        # January 8 - February 10, 2024
        # December 8, 2024 - January 10, 2025
        """
        # Parse each date ONCE
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')

        start_year = start.year
        start_month = start.strftime('%B')  # Full month name like "January"
        start_day = start.day

        end_year = end.year
        end_month = end.strftime('%B')      # Full month name like "February"
        end_day = end.day

        # Logic
        if start_year == end_year and start_month == end_month:
            date_string = f"{start_month} {start_day} - {end_day}, {start_year}"
        elif start_year == end_year and start_month != end_month:
            date_string = f"{start_month} {start_day} - {end_month} {end_day}, {end_year}"
        else:  # Different years
            date_string = f"{start_month} {start_day}, {start_year} - {end_month} {end_day}, {end_year}"

        return date_string

    def format_single_date(self, date):
        """Format a single date string."""
        date = datetime.strptime(date, '%Y-%m-%d')
        return date.strftime('%b %d, %Y')

    def get_events(self, db, filters):
        """Get events and organize them into itineraries.
        
        Args:
            db: Database connection
            filters: Dictionary containing filter parameters:
                - start_date: Optional start date (YYYY-MM-DD)
                - end_date: Optional end date (YYYY-MM-DD)
                - cities: Optional list of city names
                - weekdays: Optional list of weekday numbers (0=Monday, 6=Sunday)
                - leagues: Optional list of leagues (e.g., ['NBA', 'NHL'])
                - min_events: Minimum number of events per itinerary
        
        Returns:
            Dictionary with 'itineraries' key containing list of itinerary objects
        """
        # Extract filter parameters
        start_date = filters.get('start_date')
        end_date = filters.get('end_date')
        cities = filters.get('cities', [])
        weekdays = sorted(filters.get('weekdays', []))  # List of weekday numbers (0-6)
        leagues = filters.get('leagues', [])
        min_events = int(filters.get('min_events', 1))

        # Get events from repository
        events = self.repository.get_events(
            db,
            start_date=start_date,
            end_date=end_date,
            cities=cities if cities else None,
            leagues=leagues if leagues else None
        )

        # Filter by weekdays if specified
        if weekdays:
            events = [
                event for event in events
                if datetime.strptime(event['date'], '%Y-%m-%d').weekday() in weekdays
            ]

        # Sort events by date and time
        sorted_events = sorted(events, key=lambda x: (x['date'], x['start_time']))

        if not sorted_events:
            return {"itineraries": []}

        # Generate itineraries
        itineraries = []
        
        if weekdays:
            # Group by week ranges when weekdays are specified
            itineraries = self._create_weekly_itineraries(sorted_events, weekdays, min_events)
        else:
            # Group by date ranges when no weekdays specified
            itineraries = self._create_date_range_itineraries(sorted_events, min_events)

        return {"itineraries": itineraries}

    def _create_weekly_itineraries(self, events, weekdays, min_events):
        """Create itineraries based on weekday patterns that can wrap around weekends."""
        itineraries = []
        
        # Group events by city first
        city_events = {}
        for event in events:
            city = event['city']
            if city not in city_events:
                city_events[city] = []
            city_events[city].append(event)
        
        # For each city, find consecutive weekday patterns
        for city, city_event_list in city_events.items():
            # Sort events by date
            city_event_list.sort(key=lambda x: x['date'])
            
            # Find consecutive weekday patterns
            consecutive_groups = self._find_consecutive_weekday_groups(city_event_list, weekdays)
            
            # Create itineraries from groups that meet minimum events requirement
            for group in consecutive_groups:
                if len(group) >= min_events:
                    itinerary = self._create_itinerary(group, city)
                    itineraries.append(itinerary)
        
        return itineraries

    def _find_consecutive_weekday_groups(self, events, weekdays):
        """Find groups of events that form consecutive weekday patterns."""
        if not events:
            return []
        
        groups = []
        current_group = []
        
        for event in events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            event_weekday = event_date.weekday()
            
            if not current_group:
                # Start new group
                current_group = [event]
            else:
                # Check if this event continues the consecutive pattern
                last_event_date = datetime.strptime(current_group[-1]['date'], '%Y-%m-%d')
                
                if self._is_consecutive_weekday(last_event_date, event_date, weekdays):
                    current_group.append(event)
                else:
                    # Pattern broken, finalize current group and start new one
                    if current_group:
                        groups.append(current_group)
                    current_group = [event]
        
        # Add the last group
        if current_group:
            groups.append(current_group)
        
        return groups

    def _is_consecutive_weekday(self, last_date, current_date, weekdays):
        """Check if two dates form a consecutive pattern within the specified weekdays."""
        # Calculate days between events
        days_diff = (current_date - last_date).days
        
        # If more than 7 days apart, it's not consecutive
        if days_diff > 7:
            return False
        
        # Check if both dates are in the allowed weekdays
        last_weekday = last_date.weekday()
        current_weekday = current_date.weekday()
        
        if last_weekday not in weekdays or current_weekday not in weekdays:
            return False
        
        # Handle wrap-around cases (e.g., Fri-Tue: [4,5,6,0,1])
        if self._weekdays_wrap_around(weekdays):
            # For wrap-around patterns, check if the progression makes sense
            return self._is_valid_wrap_around_progression(last_weekday, current_weekday, weekdays, days_diff)
        else:
            # For non-wrap-around patterns, just check if they're consecutive
            return self._is_valid_consecutive_progression(last_weekday, current_weekday, weekdays, days_diff)

    def _weekdays_wrap_around(self, weekdays):
        """Check if the weekday pattern wraps around the weekend."""
        # If weekdays aren't sequential when sorted, they wrap around
        sorted_weekdays = sorted(weekdays)
        for i in range(1, len(sorted_weekdays)):
            if sorted_weekdays[i] != sorted_weekdays[i-1] + 1:
                return True
        return False

    def _is_valid_wrap_around_progression(self, last_weekday, current_weekday, weekdays, days_diff):
        """Check if progression is valid for wrap-around patterns."""
        # For wrap-around patterns like Fri-Tue [4,5,6,0,1]
        # Valid progressions: 4->5, 5->6, 6->0, 0->1, but also 4->6, 5->0, etc.
        
        # Simple approach: if both weekdays are in the pattern and within 7 days, it's valid
        # This allows for gaps (like Fri->Sun or Sat->Tue)
        return days_diff <= 7 and last_weekday in weekdays and current_weekday in weekdays

    def _is_valid_consecutive_progression(self, last_weekday, current_weekday, weekdays, days_diff):
        """Check if progression is valid for non-wrap-around patterns."""
        # For sequential patterns like Tue-Thu [1,2,3]
        # Must be consecutive days or reasonable gaps within the pattern
        return days_diff <= 7 and last_weekday in weekdays and current_weekday in weekdays

    def _create_date_range_itineraries(self, events, min_events):
        """Create itineraries for date ranges (when no weekdays specified)."""
        itineraries = []
        
        # Group events by city
        city_events = {}
        for event in events:
            city = event['city']
            if city not in city_events:
                city_events[city] = []
            city_events[city].append(event)
        
        # For each city, look for consecutive date ranges with enough events
        for city, city_event_list in city_events.items():
            # Sort events by date
            city_event_list.sort(key=lambda x: x['date'])
            
            # Group by consecutive date ranges (within 7 days of each other)
            current_group = []
            
            for event in city_event_list:
                if not current_group:
                    current_group = [event]
                else:
                    # Check if this event is within 7 days of the last event in current group
                    last_date = datetime.strptime(current_group[-1]['date'], '%Y-%m-%d')
                    current_date = datetime.strptime(event['date'], '%Y-%m-%d')
                    
                    if (current_date - last_date).days <= 7:
                        current_group.append(event)
                    else:
                        # Process current group if it has enough events
                        if len(current_group) >= min_events:
                            itinerary = self._create_itinerary(current_group, city)
                            itineraries.append(itinerary)
                        
                        # Start new group
                        current_group = [event]
            
            # Process the last group
            if current_group and len(current_group) >= min_events:
                itinerary = self._create_itinerary(current_group, city)
                itineraries.append(itinerary)
        
        return itineraries

    def _create_itinerary(self, events, city):
        """Create an itinerary object from a list of events."""
        # Sort events by date and time
        events.sort(key=lambda x: (x['date'], x['start_time']))
        
        start_date = events[0]['date']
        end_date = events[-1]['date']
        
        # Calculate total days
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        total_days = (end_dt - start_dt).days + 1
        
        # Convert events to the format expected by frontend
        formatted_events = []
        for event in events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            formatted_event = {
                'id': event['id'],
                'event_id': f"event_{event['event_id']}",
                'type': event['type'],
                'league': event['league'],
                'artist': event['artist'],
                'team': f"{event['team_away']} vs {event['team_home']}" if event['team_away'] and event['team_home'] else 'TBD',
                'venue': event['venue'],
                'date': event['date'],
                'start_time': event['start_time'],
                'end_time': event['end_time'],
                'day_of_week': event_date.strftime('%A'),
                'formatted_date': self.format_single_date(event['date'])
            }
            formatted_events.append(formatted_event)
        
        return {
            'id': f"itinerary_{str(uuid.uuid4())[:8]}",
            'city': city,
            'total_days': total_days,
            'date_range': {
                'start': start_date,
                'end': end_date,
                'formatted': self.format_date(start_date, end_date)
            },
            'events': formatted_events,
            'event_count': len(formatted_events)
        }