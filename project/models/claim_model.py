# This is our "Claim Filing Clerk".
# It handles all database operations related to food claims.

from project.db import get_db_connection

def create_claim(listing_id, user_id, quantity_claimed):
    """
    Inserts a new claim into the database.
    The database trigger will automatically handle updating the food listing's quantity.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # The SQL command to insert a new row into the claims table.
        sql = "INSERT INTO claims (listing_id, user_id, quantity_claimed) VALUES (%s, %s, %s)"
        
        # Execute the command with the provided data
        cursor.execute(sql, (listing_id, user_id, quantity_claimed))
        
        # Commit the changes to make them permanent
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return True
    except Exception as e:
        # If any error occurs, print it for debugging
        print(f"Database error in create_claim: {e}")
        return False
