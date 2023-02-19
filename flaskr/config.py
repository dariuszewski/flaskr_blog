import os


class Config:
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SECRET_KEY='dev'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr.sqlite'
    MAX_CONTENT_LENGTH = 1 * 1000 * 1000

class ProductionConfig(Config):
    SECRET_KEY='prod' # will be changed
    username = 'flaskr_admin'
    password = 'postgres'
    database = 'flaskr'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{username}:{password}@localhost:5432/{database}'
