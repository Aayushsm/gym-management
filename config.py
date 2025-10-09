class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    MONGODB_URI = 'mongodb://localhost:27017/gym_management'
    
class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False
    MONGODB_URI = 'mongodb://localhost:27017/gym_management_dev'

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGODB_URI = 'mongodb://localhost:27017/gym_management_prod'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
