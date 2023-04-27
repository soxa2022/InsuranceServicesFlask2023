from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from jwt import DecodeError
from werkzeug.exceptions import BadRequest, Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models.customers import Customer


class AuthManager:
    @staticmethod
    def create_customer(customer_data):
        customer = Customer.query.filter_by(email=customer_data["email"]).first()
        if not customer:
            customer_data["password"] = generate_password_hash(
                customer_data["password"]
            )
            customer = Customer(**customer_data)
            db.session.add(customer)
            db.session.commit()
            return customer
        raise BadRequest("The email already exists")

    @staticmethod
    def login_user(customer_data):
        customer = Customer.query.filter_by(email=customer_data["email"]).first()
        if not customer:
            raise BadRequest("Invalid email or password")
        if not check_password_hash(customer.password, customer_data["password"]):
            raise BadRequest("Invalid email or password")
        return customer

    @staticmethod
    def encode_token(customer):
        payload = {"sub": customer.id, "exp": datetime.utcnow() + timedelta(hours=24)}
        return jwt.encode(payload, config("JWT_KEY"), "HS256")

    @staticmethod
    def decode_token(token):
        try:
            return jwt.decode(token, key=config("JWT_KEY"), algorithms=["HS256"])
        except DecodeError as de:
            raise BadRequest("Invalid or missing token")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    try:
        payload = AuthManager.decode_token(token)
        customer = Customer.query.filter_by(id=payload["sub"]).first()
        if not customer:
            raise Unauthorized("Invalid or missing customer")
        return customer
    except Exception as ex:
        raise Unauthorized("Invalid or missing token")
