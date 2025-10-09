class Config:
    SECRET_KEY = 'dev-secret-key-change-in-production'
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
