import React, { useState } from 'react';
import './App.css';

function App() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [cities, setCities] = useState('');
  const [minGames, setMinGames] = useState(1);
  const [selectedWeekdays, setSelectedWeekdays] = useState([]);
  const [games, setGames] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const weekdays = [
    { value: 0, label: 'Mon' },
    { value: 1, label: 'Tue' },
    { value: 2, label: 'Wed' },
    { value: 3, label: 'Thu' },
    { value: 4, label: 'Fri' },
    { value: 5, label: 'Sat' },
    { value: 6, label: 'Sun' }
  ];

  const handleWeekdayChange = (dayValue) => {
    setSelectedWeekdays(prev => {
      // If clicking on an already selected day, deselect it and any days after it
      if (prev.includes(dayValue)) {
        return prev.filter(d => d < dayValue);
      }
      
      // If no days selected, just add this one
      if (prev.length === 0) {
        return [dayValue];
      }
      
      // Find the min and max of currently selected days
      const min = Math.min(...prev);
      const max = Math.max(...prev);
      
      // If clicking before the range, select all days from click to start of range
      if (dayValue < min) {
        return Array.from({ length: min - dayValue + 1 }, (_, i) => dayValue + i);
      }
      
      // If clicking after the range, select all days from end of range to click
      if (dayValue > max) {
        return Array.from({ length: dayValue - max + 1 }, (_, i) => max + i);
      }
      
      // If clicking within the range, do nothing
      return prev;
    });
  };

  const formatDateTime = (dateTimeStr) => {
    const date = new Date(dateTimeStr);
    return new Intl.DateTimeFormat('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      timeZoneName: 'short'
    }).format(date);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError(null);
    
    const cityList = cities.split(',')
      .map(city => city.trim())
      .filter(city => city.length > 0);

    const payload = {
      ...(startDate && { start_date: startDate }),
      ...(endDate && { end_date: endDate }),
      ...(cityList.length > 0 && { cities: cityList }),
      ...(selectedWeekdays.length > 0 && { weekdays: selectedWeekdays }),
      ...(minGames && { min_games: minGames })
    };

    try {
      const response = await fetch('http://localhost:5000/date-city', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch games data');
      }

      const data = await response.json();
      setGames(data);
    } catch (error) {
      setError('Error fetching data. Please try again.');
      setGames(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Sports Schedule Finder</h1>
      
      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-group">
          <label htmlFor="startDate">Start Date:</label>
          <input
            id="startDate"
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="endDate">End Date:</label>
          <input
            id="endDate"
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="cities">Cities (comma-separated):</label>
          <input
            id="cities"
            type="text"
            value={cities}
            onChange={(e) => setCities(e.target.value)}
            placeholder="e.g. Chicago, New York, Boston"
          />
        </div>

        <div className="form-group weekday-selector">
          <label>Select Weekday Range:</label>
          <div className="weekday-info">Select a start and end day to create a range</div>
          <div className="weekday-buttons">
            {weekdays.map(day => (
              <button
                key={day.value}
                type="button"
                className={`weekday-button ${selectedWeekdays.includes(day.value) ? 'selected' : ''}`}
                onClick={() => handleWeekdayChange(day.value)}
              >
                {day.label}
              </button>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="minGames">Minimum number of games in city</label>
          <input
            id="minGames"
            type="number"
            value={minGames}
            onChange={(e) => setMinGames(e.target.value)}
            placeholder="e.g. 1"
          />
        </div>

        <div className="form-group">
          <button type="submit" className="submit-button" disabled={loading}>
            {loading ? 'Searching...' : 'Search Games'}
          </button>
        </div>
      </form>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <div className="results-container">
        {loading && <div className="loading">Loading games...</div>}
        
        {games && Object.keys(games).length === 0 && (
          <div className="no-results">No games found matching your criteria.</div>
        )}

        {games && Object.keys(games).length > 0 && (
          <>
            <h2>Game Schedule</h2>
            {Object.entries(games).sort().map(([dateRange, citiesData]) => (
              <div key={dateRange} className="date-section">
                <h3>{dateRange.includes('(') 
                  ? dateRange // Week range format
                  : new Date(dateRange).toLocaleDateString('en-US', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })
                }</h3>
                
                {Object.entries(citiesData).sort().map(([city, cityGames]) => (
                  <div key={`${dateRange}-${city}`} className="city-section">
                    <h4>{city}</h4>
                    <div className="games-grid">
                      {cityGames.map((game) => (
                        <div key={game.game_id} className="game-card">
                          <div className="game-league">{game.league}</div>
                          <div className="game-teams">
                            <div className="team away">{game.team_away}</div>
                            <div className="vs">vs</div>
                            <div className="team home">{game.team_home}</div>
                          </div>
                          <div className="game-details">
                            <div className="game-time">{formatDateTime(game.time)}</div>
                            <div className="game-venue">{game.venue}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            ))}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
