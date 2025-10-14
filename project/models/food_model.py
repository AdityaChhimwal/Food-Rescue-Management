# This is our "Food Filing Clerk".
# It handles all database operations related to food listings.

from project.db import get_db_connection

def add_food_listing(business_id, title, description, quantity, price, expiry_time):
    """
    Inserts a new food listing into the database.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO food_listings (business_id, title, description, quantity, price, expiry_time)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (business_id, title, description, quantity, price, expiry_time))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error in add_food_listing: {e}")
        return False

def get_all_available_listings():
    """
    Fetches all food listings that are not expired and are available.
    """
    listings = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT 
                fl.id, fl.title, fl.description, fl.quantity, fl.price, fl.expiry_time,
                b.business_name AS business_name 
            FROM food_listings fl
            JOIN businesses b ON fl.business_id = b.id
            WHERE fl.expiry_time > NOW() AND fl.status = 'available'
            ORDER BY fl.expiry_time ASC
        """
        cursor.execute(sql)
        listings = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database error in get_all_available_listings: {e}")

    return listings

