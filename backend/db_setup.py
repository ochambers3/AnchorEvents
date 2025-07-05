# import sqlite3
# from flask import g
# import os

# # Define the path to the database file in the database directory at the project root level
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # print(BASE_DIR)
# DB_PATH = os.path.join(BASE_DIR, 'database', 'schedule.db')
# # print(DB_PATH)


# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(DB_PATH, check_same_thread=False)
#     return g.db

# def init_db():
#     # Initialize the db
#     db = get_db()

#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS events (
#             game_id INTEGER PRIMARY KEY,
#             league TEXT,
#             date DATE,
#             time DATETIME,
#             team_away TEXT,
#             team_home TEXT,
#             venue TEXT,
#             city TEXT
#         )
#     ''')
#     conn.commit()
#     conn.close()

#     return db