# This is our "Business Filing Clerk".


from project.db import get_db 

def find_business_by_user_id(user_id):
    """
    Finds a business profile's ID using the associated user's ID.
    """
    business = None
    try:
        conn = get_db() 
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT id FROM businesses WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        business = cursor.fetchone() 
        
        cursor.close()
        
    except Exception as e:
        print(f"Database error in find_business_by_user_id: {e}")
    
    return business

