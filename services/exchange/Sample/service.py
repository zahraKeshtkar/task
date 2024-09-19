import requests

from services.exchange.Sample.url import UrlMixin
from services.exchange.base import ExchangeServiceBase


class SampleTradingService(ExchangeServiceBase):
    service_url = 'https://your-exchange.com'

    def authenticate_user(self, user_id, user_secret):
        """Authenticate the user with the exchange service."""
        try:
            response = requests.post(
                f"{self.service_url}{UrlMixin.LOGIN}",
                json={
                    "username": user_id,
                    "password": user_secret,
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as err:
            print(f"Error during authentication: {err}")
            return None

    def execute_purchase(self, auth_token, purchase_amount):
        """Execute a purchase transaction on the exchange."""
        try:
            response = requests.post(
                f"{self.service_url}{UrlMixin.SETTLE_WITH_EXCHANGE}",
                json={"amount": purchase_amount},
                headers={"Authorization": f"Bearer {auth_token}"}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as err:
            print(f"Error executing purchase: {err}")
            return None

    def check_service_status(self):
        """Check if the exchange service is operational."""
        return False
