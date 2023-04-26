from flask import request
from flask_restful import Resource

from managers.authorization import auth
from managers.payment import PaymentManager
from models import RoleType
from schemas.request_schema.payment import PaymentCardRequestSchema
from utils.decorators import validate_schema, permission_required


class PaymentCardResource(Resource):
    @auth.login_required
    @permission_required(RoleType.customer)
    @validate_schema(PaymentCardRequestSchema)
    def post(self):
        data = request.get_json()
        return PaymentManager.transactions(data)


# TODO: implement later for ACH Transfer
class PaymentBankResource(Resource):
    pass
