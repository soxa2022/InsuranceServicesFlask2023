from db import db
from models.enum import State, VehicleType, SteeringWheelPosition


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    type_vehicle = db.Column(
        db.Enum(VehicleType), default=VehicleType.car, nullable=False
    )
    plate_number = db.Column(db.String(8), unique=True, nullable=False)
    talon_number = db.Column(db.String(9), unique=True, nullable=False)
    power = db.Column(db.String(50), nullable=False)
    engine = db.Column(db.String(50), nullable=False)
    seats = db.Column(db.String(10), nullable=False)
    registration_address = db.Column(db.String(200), nullable=False)
    talon_photo = db.Column(db.String(255), nullable=False)
    steering_wheel_position = db.Column(
        db.Enum(SteeringWheelPosition),
        default=SteeringWheelPosition.left,
        nullable=False,
    )
    usage = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum(State), default=State.pending, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    customer = db.relationship("Customer")
    is_deleted = db.Column(db.Boolean(), default=False, nullable=False)
