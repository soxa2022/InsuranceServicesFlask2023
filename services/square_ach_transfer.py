import uuid

import requests
from decouple import config

from services.square_card import SquareService


class SquareServiceBank(SquareService):
    BANK_CURRENCY = "USD"

    def __init__(self):
        super().__init__()
        self.headers = {
            "Square-Version": "2023-04-19",
            "Authorization": f"Bearer {config('SQUARE_TOKEN_BANK')}",
            "Content-Type": "application/json",
        }

    def create_payment_bank(self, amount):
        url = f"{config('BASE_URL')}"
        body = {
            "idempotency_key": str(uuid.uuid4()),
            "amount_money": {"amount": amount, "currency": self.BANK_CURRENCY},
            "source_id": "bnon:bank-nonce-ok",
            "reference_id": "123456",
            "note": "Brief description",
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["payments"]["status"]


if __name__ == "__main__":
    payment = SquareServiceBank()
    idempotency_key = str(uuid.uuid4())
    payment.create_payment_card(150, 223425234, idempotency_key)
