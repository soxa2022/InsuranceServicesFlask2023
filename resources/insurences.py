from flask import request
from flask_restful import Resource

from managers.authorization import auth
from managers.estate_insurence import EstateInsurenceManager
from managers.insurenece_base import InsurenceManager
from managers.venicle_insurence import VehicleInsurenceManager
from models import RoleType, Vehicle, Estate
from schemas.request_schema.estate import EstateRequestSchema
from schemas.request_schema.vehicle import VehicleRequestSchema
from schemas.response_schema.estate import EstateResponseSchema
from schemas.response_schema.vehicle import VehicleResponseSchema
from utils.decorators import validate_schema, permission_required


class VehicleInsurenceResource(Resource):
    @auth.login_required
    def get(self):
        insurences = VehicleInsurenceManager.get_insurences(Vehicle)
        if not insurences:
            return "Not Found Insurences"
        return VehicleResponseSchema(many=True).dump(insurences)

    @auth.login_required
    @permission_required(RoleType.customer)
    @validate_schema(VehicleRequestSchema)
    def post(self):
        data = request.get_json()
        insurence = VehicleInsurenceManager.create_vehicle_insurence(data)
        return VehicleResponseSchema().dump(insurence), 201


class EstateInsurenceResource(Resource):
    @auth.login_required
    def get(self):
        insurences = EstateInsurenceManager.get_insurences(Estate)
        if not insurences:
            return "Not Found Insurences"
        return EstateResponseSchema(many=True).dump(insurences)

    @auth.login_required
    @permission_required(RoleType.customer)
    @validate_schema(EstateRequestSchema)
    def post(self):
        data = request.get_json()
        insurence = EstateInsurenceManager.create_estate_insurence(data)
        return EstateResponseSchema().dump(insurence), 201


class InsurenceAcceptResource(Resource):
    @auth.login_required
    @permission_required(RoleType.employee)
    def get(self, pk):
        InsurenceManager.accept_insurence(pk)


class InsurenceCancelResource(Resource):
    @auth.login_required
    @permission_required(RoleType.employee)
    def get(self, pk):
        InsurenceManager.cancel_insurence(pk)


class InsurenceDeleteResource(Resource):
    @auth.login_required
    @permission_required(RoleType.admin)
    def delete(self, pk):
        InsurenceManager.delete_insurence(pk)
