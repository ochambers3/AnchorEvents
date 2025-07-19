import pytest
from api.filter_data import FilterData
from unittest.mock import MagicMock
from datetime import datetime, date

@pytest.fixture
def fake_db():
    return MagicMock()

def test_ticketmaster_filter_with_mock_data(fake_db, sample_concert_data):
    """Unit test - tests the filtering logic without database dependency"""
    # Setup
    filter_data = FilterData(fake_db)
    filter_data.data.fetch_ticketmaster_concerts = MagicMock(return_value=sample_concert_data)

    # Mock save_schedule to capture what would be saved
    captured = []
    def mock_save_schedule(data, db):
        print(f"Mock save_schedule called with:")
        print(f"  data: {data}")
        print(f"  db: {db}")
        for item in data:
            print(f"  Item types: {[(k, type(v)) for k, v in item.items()]}")
        captured.extend(data)
    
    filter_data.repository.save_schedule = mock_save_schedule

    # Call the filter method
    filter_data.ticketmaster_concert_filter(["Toronto"])
    
    print("=== CAPTURED DATA ===")
    for i, concert in enumerate(captured):
        print(f"Concert {i}:")
        for key, value in concert.items():
            print(f"  {key}: {value} (type: {type(value)})")

    # Assertions - test the data transformation logic
    assert len(captured) == 1
    concert = captured[0]
    assert concert['artist'] == "Taylor Swift"
    assert concert['venue'] == "Scotiabank Arena"
    assert concert['city'] == "Toronto"
    
    # Debug the failing assertion
    print(f"concert['start_time'] = {concert['start_time']} (type: {type(concert['start_time'])})")
    print(f"concert['date'] = {concert['date']} (type: {type(concert['date'])})")
    
    # The actual assertions
    assert concert['start_time'] == "19:30"
    assert concert['date'] == "2025-11-20"
    assert isinstance(concert['start_time'], str)
    assert isinstance(concert['date'], str)

def test_ticketmaster_filter_saves_concerts(test_db, sample_concert_data):
    """Integration test - tests the complete flow including database storage"""
    filter_data = FilterData(test_db)

    # Mock the fetch method to return our static JSON
    filter_data.data.fetch_ticketmaster_concerts = MagicMock(return_value=sample_concert_data)

    # Add debug logging to the actual repository method
    original_save_schedule = filter_data.repository.save_schedule
    
    def debug_save_schedule(schedule, db):
        print(f"=== DEBUG SAVE_SCHEDULE ===")
        print(f"Schedule length: {len(schedule)}")
        for i, game in enumerate(schedule):
            print(f"Game {i}:")
            for key, value in game.items():
                print(f"  {key}: {value} (type: {type(value)})")
        
        # Call the original method
        return original_save_schedule(schedule, db)
    
    filter_data.repository.save_schedule = debug_save_schedule

    # Call the method - this will actually save to database
    try:
        filter_data.ticketmaster_concert_filter(["Toronto"])
        print("✅ No exception thrown during save")
    except Exception as e:
        print(f"❌ Exception during save: {e}")
        import traceback
        traceback.print_exc()
        raise

    # Read the DB to verify data was stored correctly
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()

    # Print to visually verify
    print("=== INSERTED ROWS ===")
    for row in rows:
        print(dict(row))

    # Assertions - test that data was stored correctly
    assert len(rows) == 1
    assert rows[0]["venue"] == "Scotiabank Arena"
    assert rows[0]["city"] == "Toronto"
    assert rows[0]["type"] == "concert"
    assert rows[0]["league"] == None
    assert rows[0]["artist"] == "Taylor Swift"
    assert rows[0]["date"] == "2025-11-20"
    assert rows[0]["start_time"] == "19:30"