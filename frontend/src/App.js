import React, { useState } from 'react';
import './App.css'; // Import the CSS file for styling

function App() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [city, setCity] = useState('');
  const [weekend, setWeekend] = useState(false);
  const [nflWeight, setNFL] = useState('');
  const [nbaWeight, setNBA] = useState('');
  const [nhlWeight, setNHL] = useState('');
  const [games, setGames] = useState({});
  const obj = {
    "2024-10-18": {
      "Chicago": [
        {
          "date": "2024-10-18",
          "id": 12400070,
          "league": "NBA",
          "team_away": "Cleveland Cavaliers",
          "team_home": "Chicago Bulls",
          "time": "2024-10-18T19:00:00",
          "venue": "United Center"
        },
        {
          "date": "2024-10-19",
          "id": 2024020085,
          "league": "NHL",
          "team_away": "Buffalo Sabres",
          "team_home": "Chicago Blackhawks",
          "time": "2024-10-19 19:00:00",
          "venue": "United Center"
        }
      ],
      "Winnipeg": [
        {
          "date": "2024-10-18",
          "id": 2024020073,
          "league": "NHL",
          "team_away": "San Jose Sharks",
          "team_home": "Winnipeg Jets",
          "time": "2024-10-18 19:00:00",
          "venue": "Canada Life Centre"
        },
        {
          "date": "2024-10-20",
          "id": 2024020088,
          "league": "NHL",
          "team_away": "Pittsburgh Penguins",
          "team_home": "Winnipeg Jets",
          "time": "2024-10-20 14:00:00",
          "venue": "Canada Life Centre"
        }
      ]
  },
  "2024-10-25": {
    "Chicago": [
      {
        "date": "2024-10-25",
        "id": 2024020120,
        "league": "NHL",
        "team_away": "Nashville Predators",
        "team_home": "Chicago Blackhawks",
        "time": "2024-10-25 19:30:00",
        "venue": "United Center"
      },
      {
        "date": "2024-10-26",
        "id": 22400091,
        "league": "NBA",
        "team_away": "Oklahoma City Thunder",
        "team_home": "Chicago Bulls",
        "time": "2024-10-26T19:00:00",
        "venue": "United Center"
      }
    ],
    "Cleveland": [
      {
        "date": "2024-10-25",
        "id": 22400080,
        "league": "NBA",
        "team_away": "Detroit Pistons",
        "team_home": "Cleveland Cavaliers",
        "time": "2024-10-25T19:30:00",
        "venue": "Rocket Mortgage FieldHouse"
  }]}};
  // const [weightGame, setWeightGame] = useState([]);
  const [error, setError] = useState(null);

  const handleCheckedChange = () => {
    setWeekend(!weekend);
  };

  const date_city = async (event) => {
    event.preventDefault();
    
    // Construct the data payload
    let payload = {};
    if (startDate) payload.start_date = startDate;
    if (endDate) payload.end_date = endDate;
    if (city) payload.city = city;
    if (weekend) payload.weekend = weekend;
    console.log(payload);

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
      setGames(data); // Set the games state with the received data
      console.log(data);
      setError(null); // Clear any existing error messages
    } catch (error) {
      setError('Error fetching data. Please try again.');
      setGames([]); // Clear the games data on error
    }
  };

  return (
    <div className="App">
      <h1>Sportsbook Lookup</h1>
      <form onSubmit={date_city} className="form-container">

        <div className="form-group">
          <label>Start Date:</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>End Date:</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>City:</label>
          <input
            type="text"
            value={city}
            onChange={(e) => setCity(e.target.value)}
          />
        </div>
        <div className="form-group">
          <button type="submit" className="submit-button">Submit</button>
        </div>
        <div className="form-group">
          <label>Weekend:</label>
          <input
            type="checkbox"
            value={weekend}
            onChange={handleCheckedChange}
          />
        </div>
        {/* <div className="form-group">
          <label>Checkbx:</label>
          <input
            type="text"
            value={weekend}
          />
        </div> */}

      </form>

      {/* Error message display */}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {/* Display the JSON data */}
      <div className="results-container">
        <h2>Games</h2>
        {games && Object.keys(games).map((date) => (
                <div key={date} className="date-section">
                    <h2>{date}</h2>

                    {/* Iterate over the cities for the current date */}
                    {games && Object.keys(games[date]).map((city) => (
                        <div key={city} className="city-section">
                            <h3>{city}</h3>

                            {/* Iterate over the games in each city */}
                            <ul>
                                {Array.isArray(games[date][city]) && games[date][city].map((game) => (
                                    <li key={game.id} className="game-item">
                                        <div>
                                            <strong>League:</strong> {game.league}
                                        </div>
                                        <div>
                                            <strong>Match:</strong> {game.team_away} vs. {game.team_home}
                                        </div>
                                        <div>
                                            <strong>Date & Time:</strong> {new Date(game.time).toLocaleString()}
                                        </div>
                                        <div>
                                            <strong>Venue:</strong> {game.venue}
                                        </div>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </div>
            ))}
      </div>
    </div>
  );
};

export default App;


          {/*<ul>
            {games.map((game, index) => (
              <li key={index}>
                <strong>{game[1]}</strong> - {game[4]} vs {game[5]}<br />
                Date: {game[2]}, Time: {game[3]}<br />
                Venue: {game[6]}, City: {game[7]}
              </li>
            ))}
          </ul>*/}
