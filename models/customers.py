from datetime import datetime

from db import db
from models.enum import RoleType, CustomerType


class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(60), nullable=False)
    egn_or_bulstat = db.Column(db.String(13), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    driving_experience = db.Column(db.String(2), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    role = db.Column(db.Enum(RoleType), default=RoleType.customer, nullable=False)
    customer_type = db.Column(
        db.Enum(CustomerType), default=CustomerType.individual, nullable=False
    )
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
