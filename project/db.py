import mysql.connector
import os
from flask import g # 'g' is a special object to store data for a single request.

def get_db():
    """
    Gets a database connection from the application context 'g'.
    If a connection is not yet available for this request, it creates one
    and stores it. This ensures we reuse the same connection for the entire request.
    """
    if 'db' not in g:
        # No connection exists for this request yet. Create one.
        g.db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    return g.db

def close_db(e=None):
    """
    Closes the database connection at the end of the request.
    This function is automatically called by Flask.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    """
    This function registers the 'close_db' function with the Flask app
    so it gets called after each request.
    """
    app.teardown_appcontext(close_db)

