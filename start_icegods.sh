#!/bin/bash
# ICEGODS Pro Bot Startup Script

# Load environment variables
export $(grep -v '^#' ~/MasterBot/config.env | xargs)

# Run the bot in background
nohup python ~/MasterBot/icegods_pro_bot.py > ~/MasterBot/icegods_pro.log 2>&1 &

echo "🚀 ICEGODS Pro Bot running in background. Logs: ~/MasterBot/icegods_pro.log"
