# This is our "Business Filing Clerk".
# This version uses the new, robust, shared database connection.

from project.db import get_db # <-- CHANGE: Import get_db

def find_business_by_user_id(user_id):
    """
    Finds a business profile's ID using the associated user's ID.
    """
    business = None
    try:
        conn = get_db() # <-- CHANGE: Use the new get_db() function
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT id FROM businesses WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        business = cursor.fetchone() 
        
        cursor.close()
        # No conn.close() needed here anymore! The system handles it.
    except Exception as e:
        print(f"Database error in find_business_by_user_id: {e}")
    
    return business

