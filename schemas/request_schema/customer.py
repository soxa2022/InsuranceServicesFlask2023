from marshmallow import fields, validate

from schemas.base import CustomerRequestBaseSchema
from utils.validators import is_valid


class CustomerRegisterRequestSchema(CustomerRequestBaseSchema):
    name = fields.String(required=True)
    phone = fields.String(required=True)
    egn_or_bulstat = fields.String(
        required=True, validate=validate.And(validate.Length(min=9, max=13), is_valid)
    )
    address = fields.String(required=True)
    driving_experience = fields.String(required=True)


class CustomerLoginRequestSchema(CustomerRequestBaseSchema):
    pass
