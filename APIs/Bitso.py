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

    def make_request(self, url) -> dict | None:
        response = requests.get(url)
        
        if response.status_code != 200:
            return None

        return response.json()

    def get_ticker(self):
        response = self.make_request(self.base_url + "/v3/ticker/")
        
        if response is not None:
            return response["payload"]

    def create_signature(self, http_method, request_path):
        nonce =  str(int(round(time.time() * 1000)))
        message = nonce+http_method+request_path
        signature = hmac.new(self.bitso_secret.encode('utf-8'),message.encode('utf-8'),hashlib.sha256).hexdigest()
        auth_header = 'Bitso %s:%s:%s' % (self.bitso_key, nonce, signature)
        return auth_header

    
    def get_balance(self):
        request_path = "/v3/balance/"
        auth_header = self.create_signature("GET", request_path)
        response = requests.get(self.base_url + request_path, headers={"Authorization": auth_header})
        if response.status_code == 200:
            return response.json()
        else:
            return None
