import pytest
from api.filter_data import FilterData
from unittest.mock import MagicMock
from datetime import datetime

# @pytest.fixture
# def fake_db():
#     # Replace with a mock or in-memory SQLite if needed
#     return MagicMock()

def test_ticketmaster_filter_with_mock_data(db, sample_concert_data):
    # Setup
    filter_data = FilterData(db)
    filter_data.data.fetch_ticketmaster_concerts = MagicMock(return_value=sample_concert_data)

    # Mock save_schedule to inspect what gets stored
    captured = []
    filter_data.repository.save_schedule = lambda name, data, db: captured.extend(data)

    # Call the filter method
    filter_data.ticketmaster_concert_filter(["Toronto"])
    print(captured)

    # Assertions
    assert len(captured) == 1
    concert = captured[0]
    assert concert['artist'] == "Taylor Swift"
    assert concert['venue'] == "Scotiabank Arena"
    assert concert['city'] == "Toronto"
    assert concert['country'] == "Canada"
    assert concert['start_time'] == "19:30"

def test_ticketmaster_filter_saves_concerts(test_db, sample_concert_data):
    filter_data = FilterData(test_db)

    # Mock the fetch method to return our static JSON
    filter_data.data.fetch_ticketmaster_concerts = MagicMock(return_value=sample_concert_data)

    # Call the method
    filter_data.ticketmaster_concert_filter(["Toronto"])

    # Read the DB
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()

    # Print to visually verify
    print("Inserted rows:")
    for row in rows:
        print(dict(row))

    assert len(rows) == 1
    assert rows[0]["venue"] == "Scotiabank Arena"
    assert rows[0]["city"] == "Toronto"
    assert rows[0]["league"] == "Concert"