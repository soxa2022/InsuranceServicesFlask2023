import uuid

import requests
from decouple import config


class SquareService(object):
    CARD_CURRENCY = "EUR"

    def __init__(self):
        self.headers = {
            "Square-Version": "2023-04-19",
            "Authorization": f"Bearer {config('SQUARE_TOKEN_CARD')}",
            "Content-Type": "application/json",
        }

    def create_payment_card(self, amount, policy_id, idem_key):
        url = f"{config('BASE_URL')}"
        body = {
            "idempotency_key": f"{idem_key}",
            "amount_money": {"amount": amount, "currency": self.CARD_CURRENCY},
            "source_id": "cnon:card-nonce-ok",
            "autocomplete": False,
            "customer_id": "W92WH6P11H4Z77CTET0RNTGFW8",
            "reference_id": f"{policy_id}",
            "note": "Brief description",
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["payment"]["status"]

    def complete_payment(self, payment_id):
        url = f"{config('BASE_URL')}/{payment_id}/complete"
        response = requests.post(url, json=None, headers=self.headers)
        return response.json()["payment"]["status"]

    def cancel_payment(self, payment_id):
        url = f"{config('BASE_URL')}/{payment_id}/cancel"
        response = requests.post(url, json=None, headers=self.headers)
        return response.json()["payment"]["status"]

    def cancel_payment_by_key(self, key):
        url = f"{config('BASE_URL')}/cancel"
        body = {"idempotency_key": f"{key}"}
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["payment"]["status"]


if __name__ == "__main__":
    payment = SquareService()
    idempotency_key = str(uuid.uuid4())
    payment.create_payment_card(150, 223425234, idempotency_key)
