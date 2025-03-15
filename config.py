import os

class BaseConfig:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY' or 'c649d7af46bf20818931a5d9379865aa')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'

class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}