from marshmallow import fields

from schemas.base import VehicleBaseSchema


class VehicleRequestSchema(VehicleBaseSchema):
    photo = fields.Str(metadata={"Required": True})
    extension = fields.String(metadata={"Required": True})
