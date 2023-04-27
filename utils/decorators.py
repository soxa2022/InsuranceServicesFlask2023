from flask import request
from werkzeug.exceptions import BadRequest, Forbidden

from managers import authorization


def validate_schema(schema_name):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            data = request.get_json()
            schema = schema_name()
            errors = schema.validate(data)
            if not errors:
                return func(*args, **kwargs)
            raise BadRequest(errors)

        return wrapper

    return decorated_func


def permission_required(permission_role):
    def decorated_func(func):
        def wrapper(*args, **kwargs):
            current_customer = authorization.auth.current_user()
            if current_customer.role == permission_role:
                return func(*args, **kwargs)
            raise Forbidden("You not have permission to access this")

        return wrapper

    return decorated_func
