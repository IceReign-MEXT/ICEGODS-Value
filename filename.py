import time, json, os

DB_FILE = "subscriptions.json"

# Subscription plans (price in USDT)
PLANS = {
    "4h": {"duration": 4*3600, "price": 1},
    "6h": {"duration": 6*3600, "price": 1.5},
    "8h": {"duration": 8*3600, "price": 2},
    "12h": {"duration": 12*3600, "price": 3},
    "24h": {"duration": 24*3600, "price": 5},
    "weekly": {"duration": 7*24*3600, "price": 10},
    "monthly": {"duration": 30*24*3600, "price": 30},
    "yearly": {"duration": 365*24*3600, "price": 300},
    "once": {"duration": None, "price": 50}
}

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def subscribe(user_id, plan, txid):
    db = load_db()
    now = int(time.time())

    if plan not in PLANS:
        return False, "Invalid plan."

    duration = PLANS[plan]["duration"]
    expire = None if duration is None else now + duration

    db[str(user_id)] = {
        "plan": plan,
        "start": now,
        "expire": expire,
        "txid": txid
    }

    save_db(db)
    return True, f"✅ Subscribed to {plan} plan."

def check_status(user_id):
    db = load_db()
    user = db.get(str(user_id))
    if not user:
        return "❌ Not subscribed."
    
    if user["expire"] and user["expire"] < int(time.time()):
        return "⚠️ Subscription expired."
    
    return f"✅ Active Plan: {user['plan']} (tx: {user['txid']})"
