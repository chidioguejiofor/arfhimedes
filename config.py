import os


class BaseConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('APP_SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = 'app.py'


class ProductionConfig(BaseConfig):
    TESTING = False
    FLASK_ENV = 'production'
    PROPAGATE_EXCEPTIONS = True


class StagingConfig(BaseConfig):
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    FLASK_ENV = 'development'


ENV_MAPPER = {
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'development': DevelopmentConfig,
}
