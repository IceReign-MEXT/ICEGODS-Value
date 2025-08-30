import os
import logging
import asyncio
from telegram import Bot

# =========================
# Environment Variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# =========================
# Users Database (simple dict)
# =========================
users = {}  # telegram_id -> subscription

# Example: preload free users
users["123456789"] = "free"

# =========================
# Bot Notify
# =========================
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def notify_payment(telegram_id, amount, currency):
    # Upgrade subscription automatically
    users[telegram_id] = "paid"
    
    # Notify Telegram
    text = (
        f"💰 Payment received!\n\n"
        f"User: {telegram_id}\n"
        f"Amount: {amount} {currency}\n"
        f"Status: Upgraded to PAID subscription ✅"
    )
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)
    logging.info(f"[WalletMonitor] Notified payment for user {telegram_id}")

# =========================
# Bot Start (for testing)
# =========================
def start_bot():
    logging.info("[WalletMonitor] Bot started")
    for user_id, status in users.items():
        logging.info(f"[WalletMonitor] User {user_id} subscription: {status}")
