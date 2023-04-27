import enum


class RoleType(enum.Enum):
    employee = "employee"
    customer = "customer"
    admin = "admin"


class State(enum.Enum):
    pending = "pending"
    payed = "payed"
    accepted = "accepted"
    canceled = "canceled"


class CustomerType(enum.Enum):
    company = "company"
    individual = "individual"


class VehicleType(enum.Enum):
    car = "car"
    truck = "truck"
    truck_n1 = "truck_n1"
    motorbike = "motorbike"
    bus = "bus"
    trail = "trail"


class SteeringWheelPosition(enum.Enum):
    left = "left"
    right = "right"


class EstateType(enum.Enum):
    apartment = "apartment"
    house = "house"
    house_floor = "house_floor"
