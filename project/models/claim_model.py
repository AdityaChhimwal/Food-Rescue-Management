# This is our "Claim Filing Clerk".


from project.db import get_db 

def create_claim(listing_id, user_id, quantity_claimed):
    """
    Inserts a new claim into the database.
    """
    try:
        conn = get_db() 
        cursor = conn.cursor()
        
        sql = "INSERT INTO claims (listing_id, user_id, quantity_claimed) VALUES (%s, %s, %s)"
        
        cursor.execute(sql, (listing_id, user_id, quantity_claimed))
        
        # This command makes the new claim permanent for this request.
        conn.commit()
        
        cursor.close()
       
        return True
    except Exception as e:
        print(f"Database error in create_claim: {e}")
      
        get_db().rollback()
        return False

