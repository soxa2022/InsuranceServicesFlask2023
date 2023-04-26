from datetime import datetime

from db import db


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String, unique=True, nullable=False)
    policy_number = db.Column(db.String(18), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
