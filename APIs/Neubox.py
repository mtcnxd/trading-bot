import requests


class Neubox:
    def __init__(self):
        self.base_url = "https://mecanicarubio.com/api/"

    def make_request(self, url):
        response = requests.get(self.base_url + url)

        if response.status_code != 200:
            return None

        return response.json()