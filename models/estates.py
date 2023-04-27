from datetime import datetime

from db import db
from models.enum import State, EstateType


class Estate(db.Model):
    __tablename__ = "estates"
    id = db.Column(db.Integer, primary_key=True)
    type_estate = db.Column(
        db.Enum(EstateType), default=EstateType.apartment, nullable=False
    )
    policy_number = db.Column(db.String(15), default=None)
    town = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200))
    garage = db.Column(db.Boolean(), default=False, nullable=False)
    status = db.Column(db.Enum(State), default=State.pending, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    customer = db.relationship("Customer")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
