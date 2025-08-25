from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import datetime

# ====== BOT CONFIG ======
BOT_TOKEN = "8331786005:AAGPe1_OvFk8b-N49Plc69MiAGql81aY6yY"
LOG_FILE = "ICEGODS_users.log"
WHITEPAPER_LINK = "https://yourdomain.com/ICEGODS_Whitepaper.html"  # Replace with real link

# ====== LOGGING FUNCTION ======
def log_user(update: Update, command: str):
    user = update.effective_user
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    entry = f"{timestamp} | {user.id} | {user.username} | {command}\n"
    with open(LOG_FILE, "a") as f:
        f.write(entry)

# ====== COMMAND HANDLERS ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update, "/start")
    text = (
        "Welcome to IceGods EchoEyes!\n\n"
        "Available commands:\n"
        "/start - Show menu\n"
        "/stats - Check system status and uptime\n"
        "/whitepaper - Get the IceGods whitepaper\n"
        "/subscribe <plan> - Subscribe to a plan (e.g., /subscribe 1h)\n"
        "/confirm <tx> - Confirm your payment\n"
        "/wallets - See the deposit wallets\n"
        "/status - Check your subscription status"
    )
    await update.message.reply_text(text)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update, "/stats")
    uptime = datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(os.stat(__file__).st_mtime)
    await update.message.reply_text(f"System is running ✅ Uptime: {str(uptime).split('.')[0]}")

async def whitepaper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update, "/whitepaper")
    await update.message.reply_text(f"Read the IceGods whitepaper here: {WHITEPAPER_LINK}")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update, "/subscribe")
    plan = " ".join(context.args) if context.args else "No plan specified"
    await update.message.reply_text(f"Subscription requested: {plan}")

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update, "/confirm")
    tx = " ".join(context.args) if context.args else "No transaction specified"
    await update.message.reply_text(f"Payment confirmation received: {tx}")

async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update, "/wallets")
    await update.message.reply_text(
        "Deposit wallets:\n"
        "Bitcoin (BTC): bc1qes8kuftes4axt76a73xv48770m9fzherf3ld53\n"
        "Bitcoin (BTC Legacy): 3JqvK1ZAt67nipBVgZj6zWvuT8icMWBMWyu5AwYnhVss\n"
        "Ethereum (ETH): 0x08D171685e51bAf7a929cE8945CF25b3D1Ac9756"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_user(update, "/status")
    await update.message.reply_text("Your subscription is active ✅")

# ====== BUILD & RUN BOT ======
def run_bot():
    # Delete pending updates to avoid conflicts
    os.system(f"curl -s https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1")

    # Build the bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("whitepaper", whitepaper))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("confirm", confirm))
    app.add_handler(CommandHandler("wallets", wallets))
    app.add_handler(CommandHandler("status", status))

    print("👁 ICEGODS EchoEyes PROD bot is running...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
