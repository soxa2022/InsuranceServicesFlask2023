from flask_restful import Resource

from db import db
from managers.authorization import auth
from managers.stats import StatsManager
from models import RoleType, Customer, Transactions
from utils.decorators import permission_required


class InsurenceStatsResource(Resource):
    @auth.login_required
    @permission_required(RoleType.employee)
    def get(self):
        data = (
            db.session.query(
                Customer.email + " " + Customer.name,
                db.func.sum(Transactions.amount),
            )
            .select_from(Customer)
            .join(Transactions, Customer.id == Transactions.customer_id)
            .group_by(Customer.email, Customer.name)
            .all()
        )

        return StatsManager.create_img(data)
