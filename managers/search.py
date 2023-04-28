from flask import request
from sqlalchemy.sql import text

from db import db


class SearchManager:
    @staticmethod
    def get_data():
        plate_number = request.args.get("plate_number")
        email = request.args.get("email")
        results = db.session.execute(text("SELECT * FROM get_data")).all()
        results = set(results)
        if email:
            results = [res for res in results if email in res]
        if plate_number:
            results = [res for res in results if plate_number in res]
        return results
