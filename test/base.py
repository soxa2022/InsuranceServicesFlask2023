from flask_testing import TestCase

from config import create_app
from db import db
from managers.authorization import AuthManager


def generate_token(customer):
    return AuthManager.encode_token(customer)


def mock_uuid():
    return "1234-1234"


class TestAPIBase(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
