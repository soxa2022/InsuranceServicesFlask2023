import io

import matplotlib.pyplot as plt
import pandas as pd
from flask import send_file


class StatsManager:
    @staticmethod
    def create_img(data):
        df = pd.DataFrame(data)
        plt.bar(df["customer"], df["sum_amount"])
        plt.title("Customers turnover")
        plt.xlabel("customer", fontsize=10)
        plt.ylabel("Sum of Amount", fontsize=10)
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        img_buffer.seek(0)
        return send_file(img_buffer, mimetype="image/png")
