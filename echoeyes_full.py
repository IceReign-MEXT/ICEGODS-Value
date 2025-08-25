#!/usr/bin/env python3
# ICEGODS EchoEyes Bot - Full Version with Scam UserID Tracking

import datetime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# -------------------------------
# CONFIGURATION
# -------------------------------
BOT_TOKEN = "8331786005:AAGPe1_OvFk8b-N49Plc69MiAGql81aY6yY"  # Your bot token
SCAM_ALERT_LOG = "scam_users.log"

# List known scam UserIDs
SCAM_USER_IDS = [
    116568862928825447588,  # Example scam UserID
    # Add more IDs here
]

# -------------------------------
# SCAM LOGGING FUNCTION
# -------------------------------
def log_scam_user(user_id):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(SCAM_ALERT_LOG, "a") as f:
        f.write(f"⚠️ User {user_id} flagged as scam | {timestamp}\n")

# -------------------------------
# COMMAND HANDLERS
# -------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👁 Welcome to IceGods EchoEyes!\n\n"
        "Available commands:\n"
        "/start - Show this menu\n"
        "/stats - Check system status and uptime\n"
        "/whitepaper - Get the IceGods whitepaper\n"
        "/subscribe <plan> - Subscribe to a plan\n"
        "/confirm <tx> - Confirm payment\n"
        "/wallets - See deposit wallets\n"
        "/status - Check subscription status\n"
        "/checkuser - Check if a user is flagged as scam"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # For demo purposes, uptime is static. You can integrate real uptime logic.
    await update.message.reply_text("System is running ✅ Uptime: 0h 5m")

async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is the IceGods whitepaper: [link]")

async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Deposit wallets:\n"
        "SOL: ...\n"
        "ETH: ...\n"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Your subscription is active ✅")

async def check_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in SCAM_USER_IDS:
        log_scam_user(user_id)
        await update.message.reply_text(
            f"⚠️ User {user_id} is flagged as a scammer. Do NOT engage!"
        )
    else:
        await update.message.reply_text(f"User {user_id} is clean ✅")

# -------------------------------
# OPTIONAL: Auto-scan every message for scam users
# -------------------------------
async def auto_scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id in SCAM_USER_IDS:
        log_scam_user(user_id)
        await update.message.reply_text(
            f"⚠️ Alert! User {user_id} is flagged as a scammer!"
        )

# -------------------------------
# MAIN FUNCTION
# -------------------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("whitepaper", whitepaper))
    app.add_handler(CommandHandler("wallets", wallets))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("checkuser", check_user))

    # Auto-scan all messages (optional)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_scan))

    print("👁 ICEGODS EchoEyes is running...")
    app.run_polling()
