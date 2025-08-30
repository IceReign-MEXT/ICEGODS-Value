import os
from flask import Flask, request, jsonify
from telegram import Bot
import logging

# =========================
# Load Environment Variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Initialize Flask App
app = Flask(__name__)

# =========================
# Logging
# =========================
logging.basicConfig(
    filename="payment_webhook.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

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
            logging.warning(f"Invalid payload: {data}")
            return jsonify({"error": "Missing fields"}), 400

        # Send Telegram notification
        msg = (
            f"💰 Payment received!\n"
            f"User: {telegram_id}\n"
            f"Amount: {amount} {currency}\n"
            f"✅ Upgraded to PAID subscription"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
        logging.info(f"Payment processed: {msg}")

        return jsonify({"status": "success", "message": "Payment processed"}), 200

    except Exception as e:
        logging.error(f"Error in payment_webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# =========================
# Run Flask App
# =========================
if __name__ == "__main__":
    DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
    DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "5000"))
    logging.info(f"Starting Payment Webhook on {DASHBOARD_HOST}:{DASHBOARD_PORT}")
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT)
