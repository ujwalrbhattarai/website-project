"""
Configuration file for the Educational Institute Website
Modify these settings according to your needs
"""

class Config:
    # Security
    SECRET_KEY = 'your-secret-key-here-change-this-in-production'
    
    # Database - PostgreSQL Only
    # Format: postgresql://username:password@host:port/database_name
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Biratnagar-8@localhost:5432/the_innovative_group'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB max file size
    ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'webm'}
    
    # Application settings
    ITEMS_PER_PAGE = 10
    
    # Currency settings
    CURRENCY_CODE = 'NPR'
    CURRENCY_SYMBOL = 'रू'
    
    # Email settings (for future implementation)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'u2689910@gmail.com'
    MAIL_PASSWORD = 'abcd1234_4321'
    
    # Payment Gateway (for future implementation)
    # eSewa credentials
    ESEWA_MERCHANT_ID = 'your-esewa-merchant-id'
    ESEWA_SECRET_KEY = 'your-esewa-secret-key'
    
    # Khalti credentials
    KHALTI_PUBLIC_KEY = 'your-khalti-public-key'
    KHALTI_SECRET_KEY = 'your-khalti-secret-key'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Override with secure settings
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
