import os
import logging
import threading
from telegram.ext import Application, CommandHandler
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

# Dashboard Settings
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
async def start(update, context):
    await update.message.reply_text("🚀 ICEGODS MasterBot is online!")

async def wallets(update, context):
    msg = (
        f"🔗 **Tracked Wallets:**\n\n"
        f"💠 Solana: `{SOLANA_WALLETS}`\n"
        f"⛓️ Ethereum: `{ETH_WALLET}`\n"
        f"₿ Bitcoin: `{BTC_WALLET}`\n"
        f"💵 USDT: `{USDT_WALLET}`\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

async def stats(update, context):
    await update.message.reply_text("📊 Stats are coming soon!")

async def plans(update, context):
    await update.message.reply_text(
        "💰 Subscription Plans:\n"
        "BASIC: 10 USDT / 0.05 SOL / 0.003 ETH / 0.00015 BTC\n"
        "PRO: 25 USDT / 0.12 SOL / 0.007 ETH / 0.00035 BTC\n"
        "ELITE: 50 USDT / 0.25 SOL / 0.014 ETH / 0.0007 BTC"
    )

async def whitepaper(update, context):
    await update.message.reply_text("📄 Whitepaper link coming soon!")

async def subscribe(update, context):
    await update.message.reply_text("🔗 Payment addresses:\nCheck /wallet for details.")

# =========================
# Run Telegram Bot
# =========================
def run_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wallets", wallets))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("plans", plans))
    application.add_handler(CommandHandler("whitepaper", whitepaper))
    application.add_handler(CommandHandler("subscribe", subscribe))

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
