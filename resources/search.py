from flask import request
from flask_restful import Resource

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
        result = db.session.execute("SELECT * FROM get_func()")
        # result = db.session.execute("SELECT * FROM get_func() WHERE email = :email", {"email": email})
        if email:
            result = (
                result.filter_by(result.email.ilike("%" + email + "%"))
                .order_by(result.email.asc())
                .fetchall()
            )
        if plate_number:
            result = (
                result.filter_by(plate_number=plate_number)
                .order_by("plate_number")
                .fetchall()
            )

        return SearchResponseSchema(many=True).dump(result), 200
