from marshmallow import fields, validate

from models import CustomerType
from schemas.base import CustomerRequestBaseSchema
from utils.validators import is_valid


class CustomerRegisterRequestSchema(CustomerRequestBaseSchema):
    first_name = fields.String(required=True)
    middle_name = fields.String(required=True)
    last_name = fields.String(required=True)
    phone = fields.String(required=True)
    customer_type = fields.Enum(CustomerType, required=True)
    egn_or_bulstat = fields.String(required=True, validate=validate.And(validate.Length(min=9, max=13), is_valid))
    address = fields.String(required=True)
    driving_experience = fields.String(required=True)


class CustomerLoginRequestSchema(CustomerRequestBaseSchema):
    pass
