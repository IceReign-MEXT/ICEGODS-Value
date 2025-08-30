#!/usr/bin/env python3
import time
import os
import requests
from dotenv import load_dotenv
load_dotenv('./.env')

# Telegram Config
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Import modules
from BotModule1 import start_bot as start_bot1
from BotModule2 import start_bot as start_bot2
from EchoEyes import echoeyes_prod
from EmailMonitor import email_monitor
from SmartContractWatch import contract_watch
from WalletMonitor import wallet_monitor
from payment import process_payment

def send_telegram(message):
    """Send a message to Telegram."""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception as e:
        print(f"[Telegram Error] {e}")

def main():
    send_telegram("🔮 Starting ICEGODS MasterBot...")
    print("[MASTERBOT] Starting all modules...")

    # Start all bots
    start_bot1()
    start_bot2()
    echoeyes_prod.start_bot()
    email_monitor.start_bot()
    contract_watch.start_bot()
    wallet_monitor.start_bot()

    send_telegram("✅ All ICEGODS modules started. Waiting for user wallets and payments...")
    print("[MASTERBOT] All modules running. Waiting for user wallets and payments...")

    # Example: simulate checking test payments every minute
    test_payments = [
        {"telegram_id": "123456789", "amount": 20, "currency": "USD"},
    ]

    while True:
        for payment in test_payments:
            process_payment(payment["telegram_id"], payment["amount"], payment["currency"])
            send_telegram(f"[Payment] Received {payment['amount']} {payment['currency']} from user {payment['telegram_id']}")
            send_telegram(f"[Payment] User {payment['telegram_id']} upgraded to PAID subscription")
        time.sleep(60)

if __name__ == "__main__":
    main()
