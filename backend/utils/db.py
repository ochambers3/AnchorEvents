from flask import g
from db_setup import init_db

def get_db():
    """Get the database connection for the current request."""
    if 'db' not in g:
        g.db = init_db()
    return g.db

def close_db(app):
    """Register database connection cleanup with the application."""
    @app.teardown_appcontext
    def _close_db(exception):
        """Close the database connection when the request ends."""
        db = g.pop('db', None)
        if db is not None:
            db.close()
