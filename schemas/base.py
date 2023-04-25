from marshmallow import fields, Schema, validate

from models import VehicleType, SteeringWheelPosition
from models.enum import EstateType
from utils.validators import validate_password, check_email


class CustomerRequestBaseSchema(Schema):
    email = fields.Email(
        required=True,
        validate=validate.And(validate.Length(min=5, max=255), check_email),
    )
    password = fields.String(
        required=True,
        validate=validate.And(validate.Range(min=10, max=25), validate_password),
    )


class CustomerResponseBaseSchema(Schema):
    email = fields.Email(required=True)


class VehicleBaseSchema(Schema):
    type_vehicle = fields.Enum(VehicleType, required=True)
    plate_number = fields.Str(required=True, validate=validate.Range(min=7, max=8))
    talon_number = fields.Str(required=True, validate=validate.Length(10))
    power = fields.Str(required=True)
    engine = fields.Str(required=True)
    colour = fields.Str(required=True)
    seats = fields.Str(required=True)
    registration_address = fields.Str(required=True)
    steering_wheel_position = fields.Enum(SteeringWheelPosition, required=True)
    usage = fields.Str(required=True)


class EstateBaseSchema(Schema):
    type_estate = fields.Enum(EstateType, required=True)
    town = fields.Str(required=True)
    address = fields.Str(required=True)
    description = fields.Str(required=True)
