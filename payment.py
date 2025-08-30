from subscription import update_subscription
from datetime import datetime

def process_payment(telegram_id, amount, currency="USD"):
    """
    Placeholder payment processor.
    - telegram_id: User paying
    - amount: Amount paid
    - currency: Payment currency
    """
    print(f"[Payment] Received payment: {amount} {currency} from user {telegram_id}")

    # Example logic: any payment >= threshold upgrades to paid
    threshold = 10  # Example: $10
    if amount >= threshold:
        update_subscription(telegram_id, "paid", datetime.utcnow().strftime("%Y-%m-%d"))
        print(f"[Payment] User {telegram_id} upgraded to PAID subscription")
    else:
        print(f"[Payment] Amount too low. Subscription not upgraded")
