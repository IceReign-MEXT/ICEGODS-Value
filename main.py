import os
import logging
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
    await update.message.reply_text("🚀 ICEGODS MasterBot is alive!")

async def wallets(update, context):
    msg = (
        f"🔗 **Wallets Being Tracked**\n\n"
        f"💠 Solana: `{SOLANA_WALLETS}`\n"
        f"⛓️ Ethereum: `{ETH_WALLET}`\n"
        f"₿ Bitcoin: `{BTC_WALLET}`\n"
        f"💵 USDT: `{USDT_WALLET}`\n"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

def run_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("wallets", wallets))
    application.run_polling()

# =========================
# Flask Dashboard
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 ICEGODS MasterBot Dashboard Running!"

# =========================
# Run Both (Bot + Dashboard)
# =========================
if __name__ == "__main__":
    import threading
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.start()
    app.run(host=DASHBOARD_HOST, port=DASHBOARD_PORT)
