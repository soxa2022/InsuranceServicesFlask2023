from marshmallow import fields, Schema, validate

from models.enum import EstateType
from utils.validators import validate_password, check_email


class CustomerRequestBaseSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.And(validate.Length(min=5, max=255), check_email),
    )
    password = fields.Str(
        required=True,
        validate=validate.And(validate.Length(min=10, max=25), validate_password),
    )


class CustomerResponseBaseSchema(Schema):
    email = fields.Email(required=True)


class VehicleBaseSchema(Schema):
    plate_number = fields.Str(required=True, validate=validate.Length(min=7, max=8))
    talon_number = fields.Str(required=True, validate=validate.Length(10))
    power = fields.Str(required=True)
    engine = fields.Str(required=True)
    colour = fields.Str(required=True)
    seats = fields.Str(required=True)
    registration_address = fields.Str(required=True)
    usage = fields.Str(required=True)


class EstateBaseSchema(Schema):
    type_estate = fields.Enum(EstateType, required=True)
    town = fields.Str(required=True)
    address = fields.Str(required=True)
    description = fields.Str(required=True)
