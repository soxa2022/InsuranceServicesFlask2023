from marshmallow import Schema, fields


class SearchResponseSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    phone = fields.Str(required=True)
    policy_number = fields.Str(required=True)
    plate_number = fields.Str(required=True)
    talon_number = fields.Str(required=True)
    amount = fields.Float(required=True)
    payment_id = fields.Str(required=True)
