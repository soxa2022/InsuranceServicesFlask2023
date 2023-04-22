from flask import request
from flask_restful import Resource

from managers.authorization import AuthManager
from schemas.request_schema.customer import (
    CustomerLoginRequestSchema,
    CustomerRegisterRequestSchema,
)
from schemas.response_schema.customer import CustomerAuthResponseSchema
from utils.decorators import validate_schema


class RegisterResource(Resource):
    @validate_schema(CustomerRegisterRequestSchema)
    def post(self):
        data = request.get_json()
        customer = AuthManager.create_customer(data)
        token = AuthManager.encode_token(customer)
        return CustomerAuthResponseSchema().dump({"token": token})


class LoginResource(Resource):
    @validate_schema(CustomerLoginRequestSchema)
    def post(self):
        data = request.get_json()
        user = AuthManager.login_user(data)
        token = AuthManager.encode_token(user)
        return CustomerAuthResponseSchema().dump({"token": token})
