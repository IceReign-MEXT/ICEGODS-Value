#!/bin/bash
echo "🔮 Starting ICEGODS MasterBot..."

# EchoEyes
echo "👁 Starting EchoEyes..."
nohup python3 ~/MasterBot/EchoEyes/echoeyes.py > ~/MasterBot/EchoEyes/EchoEyes_log.txt 2>&1 &

# Wallet Monitor
echo "💰 Starting Wallet Monitor..."
nohup python3 ~/MasterBot/WalletMonitor/wallet_monitor.py > ~/MasterBot/WalletMonitor/WalletMonitor_log.txt 2>&1 &

# Email Monitor
echo "📧 Starting Email Monitor..."
nohup python3 ~/MasterBot/EmailMonitor/email_monitor.py > ~/MasterBot/EmailMonitor/EmailMonitor_log.txt 2>&1 &

echo "✅ All ICEGODS modules started. Logs are being saved in each module folder."

bash ~/MasterBot/start_dashboard.sh
echo "🌐 Open dashboard: http://127.0.0.1:${DASHBOARD_PORT:-8088}"
