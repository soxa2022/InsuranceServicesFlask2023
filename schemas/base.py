from marshmallow import fields, Schema, validate

from utils.validators import validate_password, check_email


class CustomerRequestBaseSchema(Schema):
    email = fields.Email(required=True, validate=validate.And(validate.Length(min=5, max=255), check_email))
    password = fields.String(required=True, validate=validate.And(validate.Length(min=10, max=25), validate_password))
    is_deleted = fields.Boolean()


class CustomerResponseBaseSchema(Schema):
    email = fields.Email(required=True)

# class InsurenceBaseSchema(Schema):
#     title = fields.Str(metadata={"Required": True})
#     description = fields.Str(metadata={"Required": True})
#     amount = fields.Float(metadata={"Required": True})
#     is_deleted = fields.Boolean()
