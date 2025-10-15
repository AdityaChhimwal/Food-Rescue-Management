# This is our "Claim Filing Clerk".
# This version uses the new, robust, shared database connection.

from project.db import get_db # <-- CHANGE: Import get_db

def create_claim(listing_id, user_id, quantity_claimed):
    """
    Inserts a new claim into the database.
    """
    try:
        conn = get_db() # <-- CHANGE: Use the new get_db() function
        cursor = conn.cursor()
        
        sql = "INSERT INTO claims (listing_id, user_id, quantity_claimed) VALUES (%s, %s, %s)"
        
        cursor.execute(sql, (listing_id, user_id, quantity_claimed))
        
        # This command makes the new claim permanent for this request.
        conn.commit()
        
        cursor.close()
        # No conn.close() needed here anymore! The system handles it.
        return True
    except Exception as e:
        print(f"Database error in create_claim: {e}")
        # If there's an error, we undo the change.
        get_db().rollback()
        return False

