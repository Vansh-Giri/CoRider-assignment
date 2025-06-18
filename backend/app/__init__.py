from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.routes.users import users_bp
from app.routes.notes import notes_bp
from app.routes.auth import auth_bp
from app.utils.database import db_instance

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure session
    app.secret_key = app.config['SECRET_KEY']
    
    # Enable CORS with credentials
    CORS(app, supports_credentials=True, origins=['http://localhost:3000'])
    
    # Initialize database connection
    db_instance.connect()
    
    # Register blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(auth_bp)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Flask Notes API is running'}, 200
    
    return app
