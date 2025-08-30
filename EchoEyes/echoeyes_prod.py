from subscription import get_subscription, is_paid

def start_bot():
    print("[EchoEyes] Bot started")

    # Load users (example using the same users.json)
    import json, os
    users_file = os.path.join(os.path.dirname(__file__), '../data/users.json')
    try:
        with open(users_file, 'r') as f:
            users = json.load(f)
        print(f"[EchoEyes] Loaded {len(users.get('users', []))} users")
    except Exception as e:
        print(f"[EchoEyes] Failed to load users.json: {e}")
        users = {"users": []}

    # Check subscription for each user
    for user in users.get("users", []):
        sub_status = get_subscription(user["telegram_id"])
        if is_paid(user["telegram_id"]):
            print(f"[EchoEyes] ✅ User {user['telegram_id']} is PAID. Full features enabled.")
            # TODO: Add full paid features here
        else:
            print(f"[EchoEyes] ⚠️ User {user['telegram_id']} is FREE. Limited features.")
            # TODO: Add limited features here
