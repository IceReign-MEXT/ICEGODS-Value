#!/bin/bash

# =========================
# ICEGODS MasterBot Launcher
# =========================

# Go to MasterBot directory
cd ~/MasterBot || exit

# Start MasterBot
echo "🔮 Starting ICEGODS MasterBot..."
nohup python3 run_all_modules.py > ~/MasterBot/nohup.out 2>&1 &

# Start Payment Webhook
echo "💰 Starting Payment Webhook..."
nohup python3 payment_webhook.py > ~/MasterBot/payment_webhook.log 2>&1 &

# Show message
echo "✅ ICEGODS MasterBot, Dashboard, and Payment Webhook started."
echo "📊 Dashboard: http://127.0.0.1:8088"
echo "💵 Payments will notify Telegram instantly."
echo "🔍 Logs: ~/MasterBot/nohup.out & ~/MasterBot/payment_webhook.log"
