import config
import requests

class Telegram:
    def __init__(self):
        self.url = f"https://api.telegram.org/bot{config.TELEGRAM_API_KEY}/sendMessage"

    def send_message(self, message: str):
        params = {
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.get(self.url, params=params)
        
        return response.json()