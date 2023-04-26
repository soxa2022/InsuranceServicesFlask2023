import uuid

from db import db
from managers.authorization import auth
from models import Transactions, Vehicle, State, Estate, Customer
from services.payment_sdk import SquareUpService
from services.send_email import send_complex_message

payment = SquareUpService()


class PaymentManager:
    @staticmethod
    def transactions(data):
        current_customer = auth.current_user()
        amount = data["amount"]
        policy_id = data["policy_number"]
        idempotency_key = str(uuid.uuid4())
        payment_id = payment.create_payment(amount, policy_id, idempotency_key)
        status = payment.complete_payment(payment_id)
        transaction = Transactions(
            payment_id=payment_id,
            policy_number=policy_id,
            status=status,
            customer_id=current_customer.id,
            amount=amount,
        )
        insurence = Vehicle.query.filter_by(
            customer_id=current_customer.id, policy_number=policy_id
        )
        if insurence:
            insurence.update({"status": State.payed})
        else:
            Estate.query.filter_by(
                customer_id=current_customer.id, policy_number=policy_id
            ).update({"status": State.payed})
        emails = [
            Customer.query.filter_by(customer_id=current_customer.id).first()["email"]
        ]
        send_complex_message(emails)
        db.session.add(transaction)
        db.session.flush()
