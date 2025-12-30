"""
Flask Application Factory
Initializes the Flask app with all extensions and configurations
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=Config):
    """
    Application factory pattern for creating Flask app instances
    
    Args:
        config_class: Configuration class to use
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Setup logging
    setup_logging(app)
    
    # Create upload directories
    create_directories(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template filters
    register_filters(app)
    
    # Log startup
    app.logger.info('Educational Institute Website startup')
    
    return app

def setup_logging(app):
    """Configure application logging"""
    if not app.debug and not app.testing:
        # Ensure logs directory exists
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Setup file handler with rotation
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

def create_directories(app):
    """Create necessary directories for uploads"""
    directories = [
        app.config['UPLOAD_FOLDER'],
        os.path.join(app.config['UPLOAD_FOLDER'], 'videos'),
        os.path.join(app.config['UPLOAD_FOLDER'], 'thumbnails'),
        os.path.join(app.config['UPLOAD_FOLDER'], 'certificates'),
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def register_blueprints(app):
    """Register all application blueprints"""
    from app.routes import (
        auth_bp,
        student_bp,
        faculty_bp,
        admin_bp,
        management_bp,
        payment_bp
    )
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(management_bp)
    app.register_blueprint(payment_bp)
    
    app.logger.info('Blueprints registered successfully')

def register_error_handlers(app):
    """Register error handlers"""
    from app.utils.error_handlers import page_not_found, internal_server_error, forbidden
    
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_error_handler(403, forbidden)

def register_filters(app):
    """Register custom Jinja2 filters"""
    from app.utils.filters import format_currency, time_ago, format_duration
    
    app.jinja_env.filters['currency'] = format_currency
    app.jinja_env.filters['timeago'] = time_ago
    app.jinja_env.filters['duration'] = format_duration
