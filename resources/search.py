from flask import request
from flask_restful import Resource
from sqlalchemy.sql import text

from db import db
from managers.authorization import auth
from models import RoleType
from schemas.response_schema.search import SearchResponseSchema
from utils.decorators import permission_required


class SearchResource(Resource):
    @auth.login_required
    @permission_required(RoleType.employee)
    def get(self):
        plate_number = request.args.get("plate_number")
        email = request.args.get("email")
        results = db.session.execute(text("SELECT * FROM get_data")).all()
        results = set(results)
        if email:
            results = [res for res in results if email in res]
        if plate_number:
            results = [res for res in results if plate_number in res]

        return SearchResponseSchema(many=True).dump(set(results)), 200
