from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from project.models.food_model import add_food_listing, get_all_available_listings
from project.models.business_model import find_business_by_user_id

food_bp = Blueprint('food', __name__, url_prefix='/food')


@food_bp.route('/add', methods=['POST'])
@jwt_required()
def add_listing():
    """
    Protected endpoint for a business to add a new food listing.
    --- THIS VERSION HAS DETAILED DEBUGGING ADDED ---
    """
    print("\n--- DEBUG: Inside /food/add route ---")
    try:
        # 1. Get the USER ID from the JWT token.
        current_user_id = get_jwt_identity()
        print(f"--- DEBUG: JWT Identity (user_id) received: {current_user_id} (Type: {type(current_user_id)}) ---")
        
        # 2. Find the corresponding BUSINESS ID by looking up the user ID.
        print(f"--- DEBUG: Calling find_business_by_user_id with user_id: {current_user_id} ---")
        business = find_business_by_user_id(current_user_id)
        
        print(f"--- DEBUG: Result from find_business_by_user_id: {business} ---")
        
        # If no business profile is found for this user, deny access.
        if not business:
            print("--- DEBUG: No business profile found. Returning 403 Forbidden. ---")
            return jsonify({'message': 'Forbidden: No business profile found for this user.'}), 403

        # We now have the correct, verified business ID.
        business_id = business['id']
        print(f"--- DEBUG: Extracted business_id: {business_id} ---")

        # 3. Get the food details from the JSON data.
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        quantity = data.get('quantity')
        price = data.get('price')
        expiry_time = data.get('expiry_time')

        if not all([title, description, quantity, price, expiry_time]):
            return jsonify({'message': 'Missing required fields'}), 400

        # 4. Call our food model with the CORRECT business_id.
        print(f"--- DEBUG: Calling add_food_listing with business_id: {business_id} ---")
        success = add_food_listing(business_id, title, description, quantity, price, expiry_time)

        if success:
            print("--- DEBUG: add_food_listing returned True. Sending 201 Created. ---")
            return jsonify({'message': 'Food listing created successfully!'}), 201
        else:
            print("--- DEBUG: add_food_listing returned False. Sending 500 Server Error. ---")
            return jsonify({'message': 'Failed to create food listing.'}), 500
            
    except Exception as e:
        print(f"--- !!! AN UNEXPECTED ERROR occurred in add_listing route: {e} !!! ---")
        return jsonify({'message': 'An internal server error occurred.'}), 500


@food_bp.route('/listings', methods=['GET'])
def get_listings():
    """
    Public endpoint to view all available food listings.
    """
    listings = get_all_available_listings()
    return jsonify(listings), 200

