import React, { useState } from 'react';
import './App.css';

function App() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [city, setCity] = useState('');
  const [weekend, setWeekend] = useState(false);
  const [games, setGames] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheckedChange = () => {
    setWeekend(!weekend);
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
    
    const payload = {
      ...(startDate && { start_date: startDate }),
      ...(endDate && { end_date: endDate }),
      ...(city && { city }),
      ...(weekend && { weekend })
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
          <label htmlFor="city">City:</label>
          <input
            id="city"
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            placeholder="Enter city name"
          />
        </div>

        <div className="form-group checkbox-group">
          <label htmlFor="weekend">
            <input
              id="weekend"
              type="checkbox"
              checked={weekend}
              onChange={handleCheckedChange}
            />
            Weekend Games Only
          </label>
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
            {Object.entries(games).sort().map(([date, citiesData]) => (
              <div key={date} className="date-section">
                <h3>{new Date(date).toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</h3>
                
                {Object.entries(citiesData).map(([city, cityGames]) => (
                  <div key={`${date}-${city}`} className="city-section">
                    <h4>{city}</h4>
                    <div className="games-grid">
                      {cityGames.map((game) => (
                        <div key={game.id} className="game-card">
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
