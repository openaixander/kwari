import requests
from django.conf import settings


class PaystackService:
    base_url = "https://api.paystack.co"

    @classmethod
    def initialize_payment(cls, email, amount, order_id, callback_url):
        url = f"{cls.base_url}/transaction/initialize"


        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }


        data = {
            "email": email,
            "amount": int(amount * 100),
            "reference": f"KWARI-ORD-{order_id}",
            "callback_url": callback_url,
        }

        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    @classmethod
    def verify_payment(cls, reference):
        url = f"{cls.base_url}/transaction/verify/{reference}"

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }

        response = requests.get(url, headers=headers)
        return response.json()