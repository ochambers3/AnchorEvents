import sqlite3
from flask import g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('schedule.db', check_same_thread=False)
    return g.db

def init_db():
    # This function can initialize tables or perform any setup logic.
    db = get_db()
    # Here, you could execute SQL to create tables, indexes, etc.
    # For example:
    # with open('schema.sql') as f:
    #     db.executescript(f.read())

    conn = sqlite3.connect('schedule.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY,
            league TEXT,
            date DATE,
            time DATETIME,
            team_away TEXT,
            team_home TEXT,
            venue TEXT,
            city TEXT
        )
    ''')
    conn.commit()
    conn.close()

    return db