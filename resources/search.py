from flask_restful import Resource

from managers.authorization import auth
from managers.search import SearchManager
from models import RoleType
from schemas.response_schema.search import SearchResponseSchema
from utils.decorators import permission_required


class SearchResource(Resource):
    @auth.login_required
    @permission_required(RoleType.employee)
    def get(self):
        results = SearchManager.get_data()
        return SearchResponseSchema(many=True).dump(set(results)), 200
