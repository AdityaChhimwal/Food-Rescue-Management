# This is our "Food Claiming Room".
# It defines the public-facing URL for users to claim food items.

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from project.models.claim_model import create_claim

# --- CHANGE 1: We are removing the url_prefix from the blueprint ---
claim_bp = Blueprint('claim', __name__)


# --- CHANGE 2: We are putting the full path on the route itself ---
@claim_bp.route('/claim', methods=['POST'])
@jwt_required() # This protects the endpoint
def make_claim():
    """
    Protected endpoint for a user to claim a quantity of a food listing.
    """
    current_user_id = get_jwt_identity()
    data = request.get_json()
    listing_id = data.get('listing_id')
    quantity_claimed = data.get('quantity_claimed')

    if not listing_id or not quantity_claimed:
        return jsonify({'message': 'listing_id and quantity_claimed are required'}), 400

    success = create_claim(listing_id, current_user_id, quantity_claimed)

    if success:
        return jsonify({'message': 'Food claimed successfully!'}), 201
    else:
        return jsonify({'message': 'Failed to claim food. Please check the listing ID.'}), 500

