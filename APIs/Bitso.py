import requests

class Bitso:
    def __init__(self):
        self.base_url = "https://api.bitso.com/v3/"

    def make_request(self, url) -> dict | None:
        response = requests.get(url)
        
        if response.status_code != 200:
            return None

        return response.json()

    def get_ticker(self):
        response = self.make_request(self.base_url + "ticker/")
        
        if response is not None:
            return response["payload"]