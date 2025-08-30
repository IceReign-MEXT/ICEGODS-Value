import requests
import os

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
LOG_FILE = os.path.expanduser("~/MasterBot/masterbot.log")

def send_last_log():
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()
    if lines:
        last_line = lines[-1]
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": last_line}
        requests.post(url, data=data)
