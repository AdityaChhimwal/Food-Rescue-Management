# This is our "User Filing Clerk".
# This version uses the new, robust, shared database connection.

from project.db import get_db # <-- CHANGE: Import get_db

def create_user(name, email, password_hash):
    """
    Inserts a new user into the database.
    """
    try:
        conn = get_db() # <-- CHANGE: Use the new get_db() function
        cursor = conn.cursor()
        
        # We assume new registrations are 'business' type for simplicity
        sql = "INSERT INTO users (name, email, password_hash, user_type) VALUES (%s, %s, %s, 'business')"
        cursor.execute(sql, (name, email, password_hash))
        
        # This command makes the new user permanent for this request.
        conn.commit() 
        
        cursor.close()
        # No conn.close() needed here anymore! The system handles it.
        return True
    except Exception as e:
        print(f"Database error in create_user: {e}")
        # If there's an error (like a duplicate email), we undo the change.
        conn.rollback()
        return False

def find_user_by_email(email):
    """
    Finds a user by their email address.
    """
    user = None # <-- FIX: Corrected variable declaration
    try:
        conn = get_db() # <-- CHANGE: Use the new get_db() function
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        
        cursor.close()
        # No conn.close() needed here anymore!
    except Exception as e:
        print(f"Database error in find_user_by_email: {e}")
    
    return user

