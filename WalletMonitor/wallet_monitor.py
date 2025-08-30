import httpx
import json
import os
from dotenv import load_dotenv
from subscription import get_subscription

load_dotenv('../config/config.env')

def start_bot():
    print("[WalletMonitor] Bot started")

    # Load users
    users_file = os.path.join(os.path.dirname(__file__), '../data/users.json')
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
        print(f"[WalletMonitor] Loaded {len(users.get('users', []))} users")
    except Exception as e:
        print(f"[WalletMonitor] Failed to load users.json: {e}")
        users = {"users": []}

    # Check subscription for each user
    for user in users.get("users", []):
        sub_status = get_subscription(user["telegram_id"])
        print(f"[WalletMonitor] User {user['telegram_id']} subscription: {sub_status}")
