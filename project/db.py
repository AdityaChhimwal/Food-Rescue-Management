# This is our dedicated utility room for the database.
# Its only job is to create a connection to our MySQL database.

import os
import mysql.connector

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        # We use os.getenv() to safely read the credentials from our .env file.
        # This keeps our password out of the main code.
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        # If the connection is successful, we return the connection object.
        return conn
    except mysql.connector.Error as err:
        # If anything goes wrong (like a wrong password or the database isn't running),
        # we print a helpful error message to the terminal.
        print(f"Database Connection Error: {err}")
        # We return 'None' to signal that the connection failed.
        return None

