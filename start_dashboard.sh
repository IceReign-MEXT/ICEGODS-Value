#!/usr/bin/env bash
set -e
cd ~/MasterBot
echo "📊 Starting ICEGODS Dashboard..."
nohup python app_dashboard.py > dashboard.log 2>&1 &
echo "✅ Dashboard on port ${DASHBOARD_PORT:-8088}. Logs: ~/MasterBot/dashboard.log"
