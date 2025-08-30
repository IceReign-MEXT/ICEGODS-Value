#!/data/data/com.termux/files/usr/bin/bash
# 🚀 ICEGODS MasterBot Railway Deploy Script

cd ~/MasterBot || exit

echo "🔗 Linking to Railway project..."
npx railway link

echo "⬆️ Deploying to Railway..."
npx railway up
