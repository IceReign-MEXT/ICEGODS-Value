# main.py
import os
import time
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import telebot
import threading
from payments import verify_eth_tx, verify_sol_tx

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
SOLANA_RPC = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")
SOL_ADDRESS = os.getenv("SOL_ADDRESS")
ETH_ADDRESS = os.getenv("ETH_ADDRESS")

WEEK_PRICE_USD = 7
MONTH_PRICE_USD = 20

if not BOT_TOKEN or not SOL_ADDRESS or not ETH_ADDRESS:
    print("❌ Missing BOT_TOKEN or payment addresses in environment. Check .env")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# --- Simple SQLite DB for subscriptions ---
DB_PATH = "subs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS subscribers (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        plan TEXT,
        expires_at TEXT
    )
    """)
    conn.commit()
    return conn

db = init_db()

def add_subscriber(user_id, username, plan, days):
    expires = datetime.utcnow() + timedelta(days=days)
    conn = db
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO subscribers (user_id, username, plan, expires_at) VALUES (?, ?, ?, ?)",
              (user_id, username, plan, expires.isoformat()))
    conn.commit()

def remove_subscriber(user_id):
    c = db.cursor()
    c.execute("DELETE FROM subscribers WHERE user_id=?", (user_id,))
    db.commit()

def is_active(user_id):
    c = db.cursor()
    c.execute("SELECT expires_at FROM subscribers WHERE user_id=?", (user_id,))
    r = c.fetchone()
    if not r:
        return False
    expires = datetime.fromisoformat(r[0])
    return datetime.utcnow() < expires

def get_expires(user_id):
    c = db.cursor()
    c.execute("SELECT expires_at FROM subscribers WHERE user_id=?", (user_id,))
    r = c.fetchone()
    return r[0] if r else None

# --- Bot commands ---
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    text = (
        "👋 Welcome to ICEGODS Value — pro wallet monitor.\n\n"
        "Plans:\n"
        f"• Weekly: ${WEEK_PRICE_USD} (7 days)\n"
        f"• Monthly: ${MONTH_PRICE_USD} (30 days)\n\n"
        "To pay, choose a plan:\n"
        "/pay_week  - Pay weekly\n"
        "/pay_month - Pay monthly\n\n"
        "After payment, send your TX hash with /verify <txhash>\n"
        "Use /status to check subscription status."
    )
    bot.send_message(msg.chat.id, text)

@bot.message_handler(commands=["status"])
def cmd_status(msg):
    active = is_active(msg.from_user.id)
    if active:
        exp = get_expires(msg.from_user.id)
        bot.reply_to(msg, f"✅ You are active until (UTC): {exp}")
    else:
        bot.reply_to(msg, "❌ You have no active subscription. Use /start to see plans.")

@bot.message_handler(commands=["pay_week"])
def cmd_pay_week(msg):
    text = (
        f"Send ${WEEK_PRICE_USD} worth of crypto to upgrade for 7 days.\n\n"
        f"Solana (SOL): `{SOL_ADDRESS}`\n"
        f"Ethereum (ETH): `{ETH_ADDRESS}`\n\n"
        "After sending, reply with `/verify <txhash>` so I can confirm automatically."
    )
    bot.send_message(msg.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["pay_month"])
def cmd_pay_month(msg):
    text = (
        f"Send ${MONTH_PRICE_USD} worth of crypto to upgrade for 30 days.\n\n"
        f"Solana (SOL): `{SOL_ADDRESS}`\n"
        f"Ethereum (ETH): `{ETH_ADDRESS}`\n\n"
        "After sending, reply with `/verify <txhash>` so I can confirm automatically."
    )
    bot.send_message(msg.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=["verify"])
def cmd_verify(msg):
    args = msg.text.split()
    if len(args) < 2:
        bot.reply_to(msg, "Usage: /verify <txhash>")
        return
    tx = args[1].strip()
    chat_id = msg.chat.id
    # Try ETH verification first, then SOL
    bot.reply_to(msg, "🔍 Verifying transaction on-chain, please wait...")
    ok, amount_usd, chain = False, 0, None
    try:
        ok_eth, eth_amount_usd = verify_eth_tx(tx, ETH_ADDRESS, ETHERSCAN_API_KEY)
    except Exception as e:
        ok_eth, eth_amount_usd = False, 0
    try:
        ok_sol, sol_amount_usd = verify_sol_tx(tx, SOL_ADDRESS, SOLANA_RPC)
    except Exception as e:
        ok_sol, sol_amount_usd = False, 0

    if ok_eth:
        ok = True
        amount_usd = eth_amount_usd
        chain = "ETH"
    elif ok_sol:
        ok = True
        amount_usd = sol_amount_usd
        chain = "SOL"

    if not ok:
        bot.send_message(chat_id, "❌ Transaction not found or not to our address. Make sure tx hash is correct and that payment went to the exact address shown.")
        return

    # Determine plan by amount: prefer month if >= month price
    if amount_usd >= MONTH_PRICE_USD:
        add_subscriber(msg.from_user.id, msg.from_user.username or "", "month", 30)
        bot.send_message(chat_id, f"✅ Payment detected on {chain}. You are upgraded to MONTH (30 days).")
    elif amount_usd >= WEEK_PRICE_USD:
        add_subscriber(msg.from_user.id, msg.from_user.username or "", "week", 7)
        bot.send_message(chat_id, f"✅ Payment detected on {chain}. You are upgraded to WEEK (7 days).")
    else:
        bot.send_message(chat_id, f"⚠️ Payment detected but amount ${amount_usd:.2f} is less than minimum plan price. Please pay at least ${WEEK_PRICE_USD} for weekly or ${MONTH_PRICE_USD} for monthly.")

# Protected command example
@bot.message_handler(commands=["monitor"])
def cmd_monitor(msg):
    if not is_active(msg.from_user.id):
        bot.reply_to(msg, "🔒 This command is for paid users only. Use /start to see subscription options.")
        return
    bot.reply_to(msg, "✅ Monitoring features are live (demo). You are a paid user.")

# Background thread: reminder checker
def reminder_loop():
    while True:
        try:
            c = db.cursor()
            c.execute("SELECT user_id, username, expires_at FROM subscribers")
            rows = c.fetchall()
            now = datetime.utcnow()
            for user_id, username, expires_at in rows:
                exp = datetime.fromisoformat(expires_at)
                days_left = (exp - now).days
                if 0 <= (exp - now).total_seconds() <= 24*3600:  # less than or equal 24h
                    try:
                        bot.send_message(user_id, f"🔔 Your subscription expires soon (UTC): {expires_at}. Renew with /pay_month or /pay_week")
                    except Exception:
                        pass
                if now > exp:
                    try:
                        bot.send_message(user_id, "⚠️ Your subscription expired. Use /pay_week or /pay_month to renew.")
                    except Exception:
                        pass
            time.sleep(60*60)  # hourly
        except Exception:
            time.sleep(60)

if __name__ == "__main__":
    t = threading.Thread(target=reminder_loop, daemon=True)
    t.start()
    print("✅ ICEGODS Value Bot Running!")
    bot.infinity_polling()