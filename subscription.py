import sqlite3
import os
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'data/subscriptions.db')

def add_user(telegram_id, wallet, subscription="free", last_payment=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO subscriptions (telegram_id, wallet, subscription, last_payment) VALUES (?, ?, ?, ?)",
              (telegram_id, wallet, subscription, last_payment))
    conn.commit()
    conn.close()

def update_subscription(telegram_id, subscription, last_payment=None):
    if last_payment is None:
        last_payment = datetime.utcnow().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE subscriptions SET subscription=?, last_payment=? WHERE telegram_id=?",
              (subscription, last_payment, telegram_id))
    conn.commit()
    conn.close()

def get_subscription(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT subscription, last_payment FROM subscriptions WHERE telegram_id=?", (telegram_id,))
    result = c.fetchone()
    conn.close()
    if result:
        subscription, last_payment = result
        # Optional: Expire paid subscriptions after 30 days
        if subscription == "paid" and last_payment:
            last_date = datetime.strptime(last_payment, "%Y-%m-%d")
            if datetime.utcnow() - last_date > timedelta(days=30):
                return "free"
        return subscription
    return "free"

def is_paid(telegram_id):
    return get_subscription(telegram_id) == "paid"
