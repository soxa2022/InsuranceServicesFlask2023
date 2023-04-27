from marshmallow import fields

from models import State
from schemas.base import VehicleBaseSchema


class VehicleResponseSchema(VehicleBaseSchema):
    id = fields.Integer(required=True)
    created_at = fields.DateTime(required=True)
    status = fields.Enum(State, by_value=True)
    customer_id = fields.Integer(required=True)
    talon_url = fields.Str(required=True)
