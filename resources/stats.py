from flask_restful import Resource
from sqlalchemy import text

from db import db
from managers.authorization import auth
from managers.stats import StatsManager
from models import RoleType
from utils.decorators import permission_required


class InsurenceStatsResource(Resource):
    @auth.login_required
    @permission_required(RoleType.employee)
    def get(self):
        data = db.session.execute(
            text(
                "SELECT concat(email,' ',name) as customer,SUM(amount) as sum_amount "
                "FROM get_data GROUP BY email,name"
            )
        ).all()
        return StatsManager.create_img(data)
