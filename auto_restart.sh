if ! pgrep -f "payment_webhook.py" > /dev/null; then
    echo "$(date) 🔄 Payment Webhook stopped. Restarting..."
    nohup python3 ~/MasterBot/payment_webhook.py >> ~/MasterBot/payment_webhook.log 2>&1 &
fi
