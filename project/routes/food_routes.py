# This is our "Food Listings Room".
# It defines the public-facing URLs for creating and viewing food listings.

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from project.models.food_model import add_food_listing, get_all_available_listings

# This blueprint will hold all our food-related routes.
food_bp = Blueprint('food', __name__, url_prefix='/food')


@food_bp.route('/add', methods=['POST'])
@jwt_required()  # This decorator protects the endpoint
def add_listing():
    """
    Protected endpoint for a business to add a new food listing.
    """
    # 1. Get the identity of the logged-in user from the JWT.
    # We assume the user's ID is the business's ID for simplicity.
    # In a real app, we might have a more complex check to ensure the user is a business.
    current_user_id = get_jwt_identity()
    
    # 2. Get the food details from the JSON data.
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    quantity = data.get('quantity')
    price = data.get('price', 0.0) # Default price to 0 if not provided
    # The expiry time should be sent in a format like 'YYYY-MM-DD HH:MM:SS'
    expiry_time = data.get('expiry_time')

    if not all([title, description, quantity, expiry_time]):
        return jsonify({'message': 'Missing required fields'}), 400

    # 3. Call our "Food Filing Clerk" to add the listing to the database.
    success = add_food_listing(current_user_id, title, description, quantity, price, expiry_time)

    if success:
        return jsonify({'message': 'Food listing created successfully!'}), 201
    else:
        return jsonify({'message': 'Failed to create food listing.'}), 500


@food_bp.route('/listings', methods=['GET'])
def get_listings():
    """
    Public endpoint to view all available food listings.
    """
    # 1. Call our "Food Filing Clerk" to get all available listings.
    listings = get_all_available_listings()
    
    # 2. Return the list of listings as JSON.
    # The `default=str` is important to handle date/time objects correctly.
    return jsonify(listings), 200
