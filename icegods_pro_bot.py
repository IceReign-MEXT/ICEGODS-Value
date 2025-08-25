import os
import json
import datetime
import asyncio
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in config.env")

# Load plans
with open("plans.json") as f:
    PLANS = json.load(f)

# Load users
USERS_FILE = "users.json"
if os.path.exists(USERS_FILE):
    with open(USERS_FILE) as f:
        USERS = json.load(f)
else:
    USERS = {"users": {}}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👁 Welcome to ICEGODS Pro Bot!\n\nCommands:\n"
        "/start – Welcome message\n"
        "/stats – Bot status\n"
        "/whitepaper – Read whitepaper\n"
        "/plans – Subscription plans\n"
        "/wallets – Deposit wallets\n"
        "/subscribe – Subscribe to a plan\n"
        "/confirm – Confirm your payment\n"
        "/status – Check subscription status\n"
        "/checkuser – Verify scam"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 ICEGODS Pro Bot is online and healthy.")

async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Whitepaper: ~/MasterBot/ICEGODS_Whitepaper.md")

async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "💳 Subscription Plans:\n"
    for plan, details in PLANS.items():
        message += f"- {plan} (30 days): {details['price_usdt']} USDT / {details['price_sol']} SOL / {details['price_eth']} ETH / {details['price_btc']} BTC\n"
    await update.message.reply_text(message)

async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "💰 Deposit wallets:\n\n"
        "SOL: 3JqvK1ZAt67nipBVgZj6zWvuT8icMWBMWyu5AwYnhVss\n"
        "ETH: 0x08D171685e51bAf7a929cE8945CF25b3D1Ac9756\n"
        "BTC: bc1qe8pf5nzj553kcyv0nl4p5cl6edrsl8ullffkmk\n"
    )
    await update.message.reply_text(message)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "💳 Usage: /subscribe <plan>\nAvailable:\n"
    for plan, details in PLANS.items():
        message += f"- {plan} (30 days): {details['price_usdt']} USDT / {details['price_sol']} SOL / {details['price_eth']} ETH / {details['price_btc']} BTC\n"
    message += "\nAfter you pay, use /confirm <txid> to activate automatically."
    await update.message.reply_text(message)

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Usage: /confirm <txid>")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user = USERS["users"].get(user_id)
    if user:
        await update.message.reply_text(f"ℹ️ Active subscription: {user['plan']} expires {user['expires_at']}")
    else:
        await update.message.reply_text("ℹ️ No subscription found. Use /plans and /subscribe to get started.")

async def checkuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Feature coming soon")

async def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("whitepaper", whitepaper))
    app.add_handler(CommandHandler("plans", plans))
    app.add_handler(CommandHandler("wallets", wallets))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("confirm", confirm))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("checkuser", checkuser))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
