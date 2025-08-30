import os
from flask import Flask, request, jsonify
from telegram import Bot

# =========================
# Load Environment Variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env")

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Initialize Flask App
app = Flask(__name__)

# =========================
# Payment Webhook Endpoint
# =========================
@app.route("/payment", methods=["POST"])
def payment_webhook():
    try:
        data = request.json
        telegram_id = data.get("telegram_id")
        amount = data.get("amount")
        currency = data.get("currency")

        if not telegram_id or not amount or not currency:
            return jsonify({"error": "Missing fields"}), 400

        # Send Telegram notification
        msg = (
            f"💰 Payment received!\n"
            f"User: {telegram_id}\n"
            f"Amount: {amount} {currency}\n"
            f"✅ Upgraded to PAID subscription"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

        # Respond to the webhook
        return jsonify({"status": "success", "message": "Payment processed"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================
# Run Flask App
# =========================
if __name__ == "__main__":
    DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
    DASHBOARD_PORT = int(os.getenv("PAYMENT_PORT", 5000))
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT)
