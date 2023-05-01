from decouple import config
from square.client import Client


class SquareUpService:
    def __init__(self):
        self.client = Client(
            access_token=config("SQUARE_TOKEN_CARD"), environment=config("SQUARE_ENV")
        )
        self.payment_id_ = None

    def create_payment(self, amount, policy_id, idempotency_key):
        res = self.client.payments.create_payment(
            body={
                "source_id": "cnon:card-nonce-ok",
                "idempotency_key": idempotency_key,
                "amount_money": {"amount": int(amount), "currency": "EUR"},
                "autocomplete": False,
                "location_id": "",
                "reference_id": policy_id,
                "note": "note",
            }
        )
        return res.body["payment"]["id"]

    def complete_payment(self, payment_id_):
        res = self.client.payments.complete_payment(payment_id=payment_id_, body={})
        return res.body["payment"]["status"]

    def cancel_payment(self, payment_id_):
        res = self.client.payments.cancel_payment(
            payment_id=payment_id_,
        )
        return res.body["payment"]["status"]


# if __name__ == "__main__":
#     payment = SquareUpService()
#     idempotency_key = str(uuid.uuid4())
#     id_= payment.create_payment(150, "223425234", idempotency_key)
#     # print(payment.cancel_payment(id_))
#     print(payment.complete_payment(id_))
