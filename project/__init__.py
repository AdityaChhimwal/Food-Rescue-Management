import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

# Initialize extensions
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    """
    This is the application factory. It creates and configures the Flask app.
    """
    app = Flask(__name__)

    # --- Configuration ---
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_fallback_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # --- Initialize Extensions ---
    bcrypt.init_app(app)
    jwt.init_app(app)

    # --- Blueprints (Route Registration) ---
    
    # Register our existing blueprints
    from project.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from project.routes.food_routes import food_bp
    app.register_blueprint(food_bp)

    # --- NEW CODE ADDED BELOW ---
    # Register our new claim blueprint
    from project.routes.claim_routes import claim_bp
    app.register_blueprint(claim_bp)
    # --- END OF NEW CODE ---

    return app

