from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from routes import routes
from services.send_reminder import schedule


class ProductionConfig:
    FLASK_ENV = "prod"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}'
        f'@localhost:{config("DB_PORT")}/{config("DB_NAME")}'
    )


class DevelopmentConfig:
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}'
        f'@localhost:{config("DB_PORT")}/{config("DB_NAME")}'
    )


class TestingConfig:
    FLASK_ENV = "testing"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{config("DB_USER")}:{config("DB_PASSWORD")}'
        f'@localhost:{config("DB_PORT")}/{config("DB_TEST_NAME")}'
    )


def create_app(config="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app)
    migrate = Migrate(app, db)
    schedule(app)
    CORS(app)
    [api.add_resource(*route) for route in routes]
    return app
