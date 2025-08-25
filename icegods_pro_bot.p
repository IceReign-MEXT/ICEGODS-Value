import os
import json
import requests
import asyncio
from datetime import datetime, timedelta
from telegram import Bot, Update
from telegram.ext import CommandHandler, ApplicationBuilder, ContextTypes

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
SOLANA_WALLETS = os.getenv("SOLANA_WALLETS", "").split(",")
ETH_WALLETS = os.getenv("ETH_WALLETS", "").split(",")
BTC_WALLETS = os.getenv("BTC_WALLETS", "").split(",")

# Validate bot token
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN not set in config.env")

# Files
USERS_FILE = "users.json"
PLANS_FILE = "plans.json"

# Load plans
with open(PLANS_FILE, "r") as f:
    PLANS = json.load(f)["plans"]

# Load users
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        USERS = json.load(f)
else:
    USERS = {"users": {}}

# Bot instance
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👁 Welcome to ICEGODS Pro Bot!\n\n"
        "Commands:\n"
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
    await update.message.reply_text(message)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 ICEGODS Pro Bot is online and healthy.")

async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Whitepaper: ~/MasterBot/ICEGODS_Whitepaper.md")

async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "💳 Subscription Plans:\n"
    for plan, data in PLANS.items():
        p = data["prices"]
        message += f"- {plan} ({data['duration_days']} days): {p['USDT']} USDT / {p['SOL']} SOL / {p['ETH']} ETH / {p['BTC']} BTC\n"
    await update.message.reply_text(message)

async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "💰 Deposit wallets:\n"
    message += f"SOL: {','.join(SOLANA_WALLETS)}\n"
    message += f"ETH: {','.join(ETH_WALLETS)}\n"
    message += f"BTC: {','.join(BTC_WALLETS)}"
    await update.message.reply_text(message)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "💳 Usage: /subscribe <plan>\nAvailable:\n"
    for plan, data in PLANS.items():
        p = data["prices"]
        message += f"- {plan} ({data['duration_days']} days): {p['USDT']} USDT / {p['SOL']} SOL / {p['ETH']} ETH / {p['BTC']} BTC\n"
    message += "\nAfter you pay, use /confirm <txid> to activate automatically."
    await update.message.reply_text(message)

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("⚠️ Usage: /confirm <txid>")
        return
    txid = context.args[0]
    user_id = str(update.effective_user.id)
    # Placeholder logic for demo
    USERS["users"][user_id] = {
        "plan": "Pro",
        "coin": "ETH",
        "amount": 0.007,
        "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "txid": txid
    }
    with open(USERS_FILE, "w") as f:
        json.dump(USERS, f, indent=2)
    await update.message.reply_text(f"✅ Payment confirmed for TXID {txid}. Subscription activated.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    user = USERS["users"].get(user_id)
    if not user:
        await update.message.reply_text("ℹ️ No subscription found. Use /plans and /subscribe to get started.")
    else:
        await update.message.reply_text(f"ℹ️ Active subscription: {user['plan']} expires {user['expires_at']}")

async def checkuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Feature coming soon")

# Run bot
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

print("🚀 ICEGODS Pro Bot started")
app.run_polling()
