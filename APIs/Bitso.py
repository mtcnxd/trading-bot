import requests
import time
import hmac
import config
import hashlib

class Bitso:
    def __init__(self):
        self.base_url = "https://api.bitso.com"
        self.bitso_key = config.API_KEY
        self.bitso_secret = config.API_SECRET

    def make_request(self, url, headers=None) -> dict | None:
        response = requests.get(url, headers=headers)
        
        if response is None:
            return None

        return response.json()

    def create_signature(self, http_method, request_path):
        nonce =  str(int(round(time.time() * 1000)))
        message = nonce+http_method+request_path
        signature = hmac.new(self.bitso_secret.encode('utf-8'),message.encode('utf-8'),hashlib.sha256).hexdigest()
        auth_header = 'Bitso %s:%s:%s' % (self.bitso_key, nonce, signature)
        return auth_header

    def get_ticker(self, book=None):
        # optional: /v3/ticker?book=btc_mxn
        response = self.make_request(self.base_url + "/v3/ticker")
        
        if response is not None:
            return response["payload"]
    
    def get_balance(self):
        request_path = "/v3/balance/"
        auth_header = self.create_signature("GET", request_path)
        response = self.make_request(self.base_url + request_path, headers={"Authorization": auth_header})
        
        if response is not None:
            return response["payload"]

    def get_orders(self):
        self.base_url + "/v3/orders"
        pass

    def cancel_order(self):
        self.base_url + "/v3/orders/{id}/"
        pass

    def get_trades(self):
        self.base_url + "/v3/trades"
        pass

    def place_order(self):
        self.base_url + "/v3/orders"
        pass

    def get_account_status(self):
        response  = self.make_request(self.base_url + "/v3/account_status", headers={"Authorization": self.create_signature("GET", "/v3/account_status")})
        print(response)