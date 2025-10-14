# This is our "User Filing Clerk".
# It contains functions that interact directly with the 'users' table in our database.

from project.db import get_db_connection

def create_user(name, email, hashed_password):
    """
    Inserts a new user into the users table.
    Takes a name, email, and a pre-hashed password as arguments.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    
    try:
        cursor.execute(sql, (name, email, hashed_password))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

# --- NEW FUNCTION ADDED BELOW ---

def find_user_by_email(email):
    """
    Finds a user in the database by their email address.
    Returns the user's data if found, otherwise returns None.
    """
    conn = get_db_connection()
    # We use a dictionary cursor to get results as a dictionary (e.g., {'id': 1, 'name': 'Test'})
    # which is easier to work with than a tuple.
    cursor = conn.cursor(dictionary=True)
    
    sql = "SELECT * FROM users WHERE email = %s"
    
    try:
        # We only need to find one user, so the tuple has only one item.
        cursor.execute(sql, (email,))
        
        # 'fetchone()' retrieves the first matching row from the query results.
        user = cursor.fetchone()
        
        # Return the user dictionary if found, or None if no user matched the email.
        return user
    except Exception as e:
        print(f"Error finding user: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

