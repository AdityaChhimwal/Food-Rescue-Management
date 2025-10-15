from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from project import bcrypt
from project.models.user_model import create_user, find_user_by_email


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Handles new user registration.
    """
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not all([name, email, password]):
        return jsonify({'message': 'All fields are required'}), 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    success = create_user(name, email, hashed_password)

    if success:
        return jsonify({'message': 'User created successfully!'}), 201
    else:
        return jsonify({'message': 'User with this email already exists or an error occurred'}), 409


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Handles user login and returns a JWT access token if successful.
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = find_user_by_email(email)

    if not user or not bcrypt.check_password_hash(user['password_hash'], password):
        return jsonify({'message': 'Invalid credentials'}), 401
    

    access_token = create_access_token(identity=str(user['id']))
    
    return jsonify({'access_token': access_token})

