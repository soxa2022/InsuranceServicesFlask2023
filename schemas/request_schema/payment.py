from marshmallow import Schema, fields, validate


class PaymentCardRequestSchema(Schema):
    first_name = fields.String(required=True)
    middle_name = fields.String(required=True)
    last_name = fields.String(required=True)
    card_brand = fields.String(required=True)
    card_number = fields.String(required=True)
    exp_month = fields.String(required=True)
    exp_year = fields.String(required=True)
    cvv = fields.String(required=True)
    avs = fields.String(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=1))
    currency = fields.String(required=True)
    policy_number = fields.String(required=True)
