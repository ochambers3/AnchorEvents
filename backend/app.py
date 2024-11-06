import sqlite3
from flask import Flask, g
from flask_cors import CORS
from service.game_service import GameService
from api.filter_data import FilterData
from repository.db_setup import init_db
from controller.game_controller import GameController


def main():
    # Create the Flask app instance
    app = Flask(__name__)
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)


    # Create an application context
    with app.app_context():
        # Get the database instance
        db = init_db()

        #Passing database to api to get data
        # api = FilterData(db)
        # api.nba_filter()
        # api.nhl_filter()
        # api.nba_filter()

    # Pass the db instance to the controller as well
    controller = GameController(db, app)

    @controller.app.teardown_appcontext
    def close_db(exception):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    controller.app.run(debug=True)


if __name__ == "__main__":
    main()


#THings to do:
#The code, as of now, returns blocks without a gap greater than block_size
#Raps and Leafs play back to back from 2024-12-01 to 2024-12-07 so this is one "Block"
#Make city specific/Team specific
#Differentiate between New York Rangers and New Yourk Islanders
#Add comments

#If weekend, only return games with more than one game.
#Print json data well