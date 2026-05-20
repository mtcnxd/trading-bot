import requests
import time
import hmac
import config
import hashlib

class Bitso:
    def __init__(self):
        self.base_url = "https://api.bitso.com"
        self.bitso_key = config.BITSO_KEY
        self.bitso_secret = config.BITSO_SECRET

    def make_request(self, url, headers=None) -> dict | None:
        response = requests.get(url, headers=headers)

        if response is None:
            return None

        return response.json()

    def create_signature(self, http_method, request_path):
        nonce = str(int(round(time.time() * 1000)))
        message = nonce+http_method+request_path
        signature = hmac.new(self.bitso_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        auth_header = 'Bitso %s:%s:%s' % (self.bitso_key, nonce, signature)
        return auth_header

    def get_ticker(self, book=None):
        if book is not None:
            response = self.make_request(self.base_url + "/v3/ticker?book=" + book)
        else:
            response = self.make_request(self.base_url + "/v3/ticker")

        if response is not None:
            return response["payload"]

    def get_balance(self):
        response = self.make_request(
            self.base_url + "/v3/balance/",
            headers={"Authorization": self.create_signature("GET", "/v3/balance/")}
        )

        if response is not None:
            return response["payload"]

    def get_orders(self):
        response = self.make_request(
            self.base_url + "/v3/orders", headers={"Authorization": self.create_signature("GET", "/v3/orders")}
        )

        if not response:
            raise Exception("API request failed or response is none")

        if not response['success']:
            raise Exception(response['error']['message'])

        return response['payload']

    def cancel_order(self):
        self.base_url + "/v3/orders/{id}/"

    def get_trades(self, book, limit=20) -> dict:
        response = self.make_request(
            self.base_url + f"/v3/trades?book={book}&limit={limit}",
            headers={"Authorization": self.create_signature("GET", f"/v3/trades?book={book}&limit={limit}")}
        )

        if not response:
            raise Exception("API request failed or response is none")

        if not response['success']:
            raise Exception(response['error']['message'])

        return response['payload']

    def place_order(self) -> dict:
        response = self.make_request(
            self.base_url + "/v3/orders", headers={"Authorization": self.create_signature("POST", "/v3/orders")}
        )

        if response is not None:
            return response['payload']

    def get_account_status(self) -> dict:
        response = self.make_request(
            self.base_url + "/v3/account_status", headers={"Authorization": self.create_signature("GET", "/v3/account_status")}
        )

        if response is not None:
            return response['payload']

    def get_user_trades(self, limit=20) -> dict:
        response = self.make_request(
            self.base_url + f"/v3/user_trades?limit={limit}", headers={"Authorization": self.create_signature("GET", f"/v3/user_trades?limit={limit}")}
        )

        if response is not None:
            return response['payload']