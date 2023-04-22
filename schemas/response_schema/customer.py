from marshmallow import Schema, fields


class CustomerAuthResponseSchema(Schema):
    token = fields.Str(required=True)
