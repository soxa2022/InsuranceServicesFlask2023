import factory

from db import db
from models import Customer, RoleType, State, Vehicle, VehicleType, Estate, EstateType, Transactions
from test.base import mock_uuid


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        obj = super().create(**kwargs)
        db.session.add(obj)
        db.session.flush()
        return obj


class CustomerFactory(BaseFactory):
    class Meta:
        model = Customer

    id = factory.Sequence(lambda n: n)
    name = f"{factory.Faker('first_name')} {factory.Faker('last_name')}"
    egn_or_bulstat = "8505206110"
    email = factory.Faker("email")
    phone = str(factory.Faker("random_number", digits=8))
    password = factory.Faker("password")
    role = RoleType.customer
    address = factory.Faker("address")
    driving_experience = "10"
    is_deleted = False


def get_customer_id():
    return CustomerFactory().id


class VehicleFactory(BaseFactory):
    class Meta:
        model = Vehicle

    type_vehicle = VehicleType.car
    plate_number = str(factory.Faker("random_number", digits=8))
    talon_number = str(factory.Faker("random_number", digits=10))
    power = "150"
    engine = "1800"
    seats = 6
    colour = "white"
    registration_address = factory.Faker("address")
    talon_photo = factory.Faker("url")
    usage = factory.Faker("word")
    created_at = factory.Faker("date_time")
    status = State.pending
    customer_id = factory.LazyFunction(get_customer_id)
    is_deleted = False


class EstateFactory(BaseFactory):
    class Meta:
        model = Estate

    type_estate = EstateType.apartment
    town = factory.Faker("city")
    address = factory.Faker("address")
    description = factory.Faker("sentence")
    created_at = factory.Faker("date_time")
    status = State.pending
    customer_id = factory.LazyFunction(get_customer_id)
    garage = False
    is_deleted = False


class TransactionFactory(BaseFactory):
    class Meta:
        model = Transactions

    id = factory.Sequence(lambda n: n)
    payment_id = mock_uuid()
    policy_number = str(factory.Faker("random_number", digits=18))
    status = "COMPLETED"
    amount = factory.Faker("pyfloat")
    create_at = factory.Faker("date_time")
    complaint_id = factory.LazyFunction(get_customer_id())
    is_deleted = False
