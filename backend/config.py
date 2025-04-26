# config.py
class Config:
    DEBUG = False
    DATABASE_URI = '../database/schedule.db'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = ':memory:'