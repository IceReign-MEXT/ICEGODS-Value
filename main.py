import os
import logging
import threading
from telegram import BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from flask import Flask

# =========================
# Load Environment Variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Wallets
SOLANA_WALLETS = os.getenv("SOLANA_WALLETS")
ETH_WALLET = os.getenv("ETH_WALLET")
BTC_WALLET = os.getenv("BTC_WALLET")
USDT_WALLET = os.getenv("USDT_WALLET")

# Subscription Plans
PLAN_BASIC_USDT = os.getenv("PLAN_BASIC_USDT")
PLAN_BASIC_SOL = os.getenv("PLAN_BASIC_SOL")
PLAN_BASIC_ETH = os.getenv("PLAN_BASIC_ETH")
PLAN_BASIC_BTC = os.getenv("PLAN_BASIC_BTC")

PLAN_PRO_USDT = os.getenv("PLAN_PRO_USDT")
PLAN_PRO_SOL = os.getenv("PLAN_PRO_SOL")
PLAN_PRO_ETH = os.getenv("PLAN_PRO_ETH")
PLAN_PRO_BTC = os.getenv("PLAN_PRO_BTC")

PLAN_ELITE_USDT = os.getenv("PLAN_ELITE_USDT")
PLAN_ELITE_SOL = os.getenv("PLAN_ELITE_SOL")
PLAN_ELITE_ETH = os.getenv("PLAN_ELITE_ETH")
PLAN_ELITE_BTC = os.getenv("PLAN_ELITE_BTC")

# Dashboard
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8088"))

# =========================
# Logging
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# =========================
# Telegram Bot Handlers
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 ICEGODS MasterBot is live!")

async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"🔗 **Wallets Being Tracked**\n\n"
        f"💠 Solana: `{SOLANA_WALLETS}`\n"
        f"⛓️ Ethereum: `{ETH_WALLET}`\n"
        f"₿ Bitcoin: `{BTC_WALLET}`\n"
        f"💵 USDT: `{USDT_WALLET}`\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"💰 **Subscription Plans**\n\n"
        f"**Basic:** {PLAN_BASIC_USDT} USDT | {PLAN_BASIC_SOL} SOL | {PLAN_BASIC_ETH} ETH | {PLAN_BASIC_BTC} BTC\n"
        f"**Pro:** {PLAN_PRO_USDT} USDT | {PLAN_PRO_SOL} SOL | {PLAN_PRO_ETH} ETH | {PLAN_PRO_BTC} BTC\n"
        f"**Elite:** {PLAN_ELITE_USDT} USDT | {PLAN_ELITE_SOL} SOL | {PLAN_ELITE_ETH} ETH | {PLAN_ELITE_BTC} BTC\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 Whitepaper: [View Here](https://example.com/whitepaper)", parse_mode="Markdown")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💳 Subscribe using the payment addresses. Check /plans for details.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Your subscription status is: PAID (example)")

async def checkuser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔎 Checking user subscription... Done.")

# =========================
# Run Telegram Bot
# =========================
def run_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wallets", wallets))
    application.add_handler(CommandHandler("plans", plans))
    application.add_handler(CommandHandler("whitepaper", whitepaper))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("checkuser", checkuser))

    # Register commands in Telegram menu
    commands = [
        BotCommand("start", "Start ICEGODS MasterBot"),
        BotCommand("wallets", "Show tracked wallet balances"),
        BotCommand("plans", "Show subscription plans"),
        BotCommand("whitepaper", "View whitepaper"),
        BotCommand("subscribe", "Upgrade your subscription"),
        BotCommand("status", "Check subscription status"),
        BotCommand("checkuser", "Verify user subscription"),
    ]
    application.bot.set_my_commands(commands)

    # Run bot
    application.run_polling()

# =========================
# Flask Dashboard
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 ICEGODS MasterBot Dashboard Running!"

# =========================
# Run Bot + Dashboard
# =========================
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT)
