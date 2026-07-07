from Services.Telegram import Telegram
import datetime
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita conectarse realmente
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

now = datetime.datetime.now()
time_formatted=now.strftime("%Y-%m-%d %H:%M:%S")
ip = get_local_ip()

Telegram().send_message(f"System has been started at: {time_formatted}\nWith local IP: {ip}")
