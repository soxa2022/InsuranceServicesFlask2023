import uuid

from db import db
from managers.authorization import auth
from models import Transactions, Vehicle, State, Estate, Customer
from services.payment_sdk import SquareUpService
from services.send_email import send_complex_message

payment = SquareUpService()
text = "You pay for insurene policy number: "


class PaymentManager:
    @staticmethod
    def transactions(data):
        current_customer = auth.current_user()
        amount = data["amount"]
        policy_id = data["policy_number"]
        idempotency_key = str(uuid.uuid4())
        payment_id = payment.create_payment(amount, policy_id, idempotency_key)
        status = payment.complete_payment(payment_id)
        insurence = Vehicle.query.filter_by(
            customer_id=current_customer.id, policy_number=policy_id)
        if not insurence:
            insurence = Estate.query.filter_by(
                customer_id=current_customer.id, policy_number=policy_id)
        else:
            raise Exception("Insurence not found")

        transaction = Transactions(
            payment_id=payment_id,
            policy_number=policy_id,
            status=status,
            insurence_id=insurence.id,
            amount=amount,
        )
        insurence.update({"status": State.payed})
        emails = [Customer.query.filter_by(id=current_customer.id).first().email]
        status = send_complex_message(emails, f"{text}{policy_id}")
        db.session.add(transaction)
        db.session.commit()
        return status
