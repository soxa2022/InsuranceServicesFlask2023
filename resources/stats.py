import io

import matplotlib.pyplot as plt
import pandas as pd
from flask_restful import Resource

from db import db
from managers.authorization import auth
from models import RoleType
from utils.decorators import permission_required
from utils.helpers import encode_image


class InsurenceStatsResource(Resource):
    @auth.login_required
    @permission_required(RoleType.employee)
    def get(self):
        data = db.session.execute("SELECT * FROM get_func()")
        df = pd.DataFrame(data)
        grouped_df = df.groupby("email")["amount"].agg(["sum"])
        grouped_df.columns = ["sum_of_amounts"]

        plt.bar(grouped_df["email"], grouped_df["sum_of_amounts"])
        plt.title("Customer turnover")
        plt.xlabel("Email")
        plt.ylabel("Sum of Amount")
        plt.xticks(rotation=45)

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        img_buffer.seek(0)
        # return send_file(img_buffer, mimetype='image/png')
        return encode_image(img_buffer)
