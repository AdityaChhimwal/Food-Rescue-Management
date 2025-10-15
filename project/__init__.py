import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv

# --- NEW: Import the entire db module ---
from . import db

load_dotenv()

bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    CORS(app) 

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'a_fallback_secret_key')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    bcrypt.init_app(app)
    jwt.init_app(app)

    # --- NEW: Initialize our database manager ---
    db.init_app(app)

    # Register Blueprints
    from project.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from project.routes.food_routes import food_bp
    app.register_blueprint(food_bp)
    
    from project.routes.claim_routes import claim_bp
    app.register_blueprint(claim_bp)

    return app

