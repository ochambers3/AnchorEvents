import os
from pathlib import Path

class Config:
    """Base configuration class."""
    DEBUG = False
    TESTING = False
    
    # Database configuration
    BASE_DIR = Path(__file__).parent.parent
    DATABASE_URI = os.getenv('DATABASE_URI', str(BASE_DIR / 'database' / 'schedule.db'))
    
    # API configuration
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 30))
    
    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = ':memory:'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # Add production-specific settings here

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}