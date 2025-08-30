import os
import logging
import threading
from telegram import Bot, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update
from flask import Flask

# =========================
# Load Environment Variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SOLANA_WALLETS = os.getenv("SOLANA_WALLETS")
ETH_WALLET = os.getenv("ETH_WALLET")
BTC_WALLET = os.getenv("BTC_WALLET")
USDT_WALLET = os.getenv("USDT_WALLET")

DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8088"))

# =========================
# Logging
# =========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# =========================
# Telegram Bot Handlers
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 ICEGODS MasterBot is alive!")

async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        f"🔗 **Wallets Being Tracked**\n\n"
        f"💠 Solana: `{SOLANA_WALLETS}`\n"
        f"⛓️ Ethereum: `{ETH_WALLET}`\n"
        f"₿ Bitcoin: `{BTC_WALLET}`\n"
        f"💵 USDT: `{USDT_WALLET}`\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💳 Subscription plans coming soon...")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Your subscription status: PAID")  # placeholder

async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📄 ICEGODS whitepaper: [link]")

async def plans(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 Subscription plans:\nBasic / Pro / Elite")  # placeholder

# =========================
# Set Bot Commands (BotFather)
# =========================
def set_bot_commands():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    commands = [
        BotCommand("start", "🚀 Start the ICEGODS MasterBot"),
        BotCommand("wallets", "🔗 Show tracked wallet balances"),
        BotCommand("subscribe", "💳 Subscribe to a plan"),
        BotCommand("status", "📊 Check subscription status"),
        BotCommand("whitepaper", "📄 Get ICEGODS whitepaper"),
        BotCommand("plans", "💰 Show subscription plans")
    ]
    bot.set_my_commands(commands)
    print("✅ Bot commands updated in BotFather!")

# =========================
# Run Telegram Bot
# =========================
def run_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wallets", wallets))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("whitepaper", whitepaper))
    application.add_handler(CommandHandler("plans", plans))

    # Register commands with BotFather
    set_bot_commands()

    # Start polling
    application.run_polling()

# =========================
# Flask Dashboard
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 ICEGODS MasterBot Dashboard Running!"

# =========================
# Run Both Bot + Dashboard
# =========================
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT)
