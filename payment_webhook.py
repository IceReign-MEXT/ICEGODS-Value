#!/usr/bin/env python3
from flask import Flask, request, jsonify
from payment import process_payment

app = Flask(__name__)

@app.route("/payment", methods=["POST"])
def payment_webhook():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    telegram_id = data.get("telegram_id")
    amount = data.get("amount")
    currency = data.get("currency")

    if not telegram_id or not amount or not currency:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    # Process the payment
    process_payment(telegram_id, amount, currency)

    return jsonify({"status": "success", "message": f"Payment processed for {telegram_id}"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
