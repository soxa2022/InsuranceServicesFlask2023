from marshmallow import Schema, fields


class PaymentCardRequestSchema(Schema):
    first_name = fields.String(required=True)
    middle_name = fields.String(required=True)
    last_name = fields.String(required=True)
    card_brand = fields.String(required=True)
    card_number = fields.Integer(required=True)
    exp_month = fields.Integer(required=True)
    exp_year = fields.Integer(required=True)
    cvv_status = fields.Integer(required=True)
    avs_status = fields.Integer(required=True)
    amount = fields.Float(required=True)
    currency = fields.String(required=True)
    policy_number = fields.String(required=True)
