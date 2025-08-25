import asyncio
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.request import HTTPXRequest
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

# 🔑 Telegram Bot Token
BOT_TOKEN = "8331786005:AAGPe1_OvFk8b-N49Plc69MiAGql81aY6yY"

# 📌 Chat ID (set after /start)
ADMIN_CHAT_ID = 123456789

# 📌 Wallets
WALLETS = {
    "Solana": [
        "4tUTqBSzqz8eXbZPVdP2e5tiNRbFK3j5GFTqLEKubUzy",
        "G2uKjynRQs3GUTcCHGV7dyMsefvKskfMz1RakGEYMCBo"
    ],
    "Ethereum": [
        "0x08D171685e51bAf7a929cE8945CF25b3D1Ac9756"
    ],
    "Bitcoin": [
        "bc1qg6mvxr0taxv2x4fmwsg5y4rdf52tt0h45cqnvv"
    ]
}

# 🚀 Solana RPC
SOLANA_RPC = "https://api.mainnet-beta.solana.com"

# === Store Last Balances for Alerts ===
last_balances = {}

# === Price Fetch ===
def get_prices() -> dict:
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"
    try:
        resp = requests.get(url, timeout=20).json()
        return {
            "BTC": resp["bitcoin"]["usd"],
            "ETH": resp["ethereum"]["usd"],
            "SOL": resp["solana"]["usd"]
        }
    except:
        return {"BTC": 0, "ETH": 0, "SOL": 0}

# === Balance Functions ===
async def get_solana_balance(wallet: str) -> float:
    async with AsyncClient(SOLANA_RPC) as client:
        pubkey = Pubkey.from_string(wallet)
        balance = await client.get_balance(pubkey)
        return balance.value / 1e9

def get_eth_balance(wallet: str) -> float:
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={wallet}&tag=latest&apikey=YourApiKeyToken"
    try:
        resp = requests.get(url, timeout=20).json()
        if resp["status"] == "1":
            return int(resp["result"]) / 1e18
    except:
        return 0.0
    return 0.0

def get_btc_balance(wallet: str) -> float:
    url = f"https://blockchain.info/q/addressbalance/{wallet}"
    try:
        resp = requests.get(url, timeout=20).text
        return int(resp) / 1e8
    except:
        return 0.0

# === Report Builder ===
async def build_report() -> str:
    prices = get_prices()
    msg = "👁 ICEGODS EchoEyes Balance Report 👁\n\n"

    for wallet in WALLETS["Solana"]:
        bal = await get_solana_balance(wallet)
        usd = bal * prices["SOL"]
        msg += f"💠 Solana {wallet[:4]}...{wallet[-4:]}: {bal:.4f} SOL (${usd:,.2f})\n"

    for wallet in WALLETS["Ethereum"]:
        bal = get_eth_balance(wallet)
        usd = bal * prices["ETH"]
        msg += f"⚡ Ethereum {wallet[:6]}...{wallet[-4:]}: {bal:.4f} ETH (${usd:,.2f})\n"

    for wallet in WALLETS["Bitcoin"]:
        bal = get_btc_balance(wallet)
        usd = bal * prices["BTC"]
        msg += f"₿ Bitcoin {wallet[:6]}...{wallet[-4:]}: {bal:.4f} BTC (${usd:,.2f})\n"

    return msg

# === Save Logs ===
def save_log(message: str):
    with open("icegods_logs.txt", "a") as f:
        f.write(f"[{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC]\n{message}\n\n")

# === Balance Change Detector ===
async def detect_changes(app: Application):
    prices = get_prices()
    changes = []

    # Solana
    for wallet in WALLETS["Solana"]:
        bal = await get_solana_balance(wallet)
        prev = last_balances.get(wallet, None)
        if prev is not None and abs(bal - prev) > 0:
            usd = bal * prices["SOL"]
            changes.append(f"⚠️ Solana {wallet[:4]}...{wallet[-4:]} changed!\nOld: {prev:.4f} → New: {bal:.4f} SOL (${usd:,.2f})")
        last_balances[wallet] = bal

    # Ethereum
    for wallet in WALLETS["Ethereum"]:
        bal = get_eth_balance(wallet)
        prev = last_balances.get(wallet, None)
        if prev is not None and abs(bal - prev) > 0:
            usd = bal * prices["ETH"]
            changes.append(f"⚠️ Ethereum {wallet[:6]}...{wallet[-4:]} changed!\nOld: {prev:.4f} → New: {bal:.4f} ETH (${usd:,.2f})")
        last_balances[wallet] = bal

    # Bitcoin
    for wallet in WALLETS["Bitcoin"]:
        bal = get_btc_balance(wallet)
        prev = last_balances.get(wallet, None)
        if prev is not None and abs(bal - prev) > 0:
            usd = bal * prices["BTC"]
            changes.append(f"⚠️ Bitcoin {wallet[:6]}...{wallet[-4:]} changed!\nOld: {prev:.4f} → New: {bal:.4f} BTC (${usd:,.2f})")
        last_balances[wallet] = bal

    if changes:
        msg = "\n\n".join(changes)
        save_log("🔔 ALERT\n" + msg)
        await app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg)

# === Telegram Commands ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global ADMIN_CHAT_ID
    ADMIN_CHAT_ID = update.effective_chat.id
    await update.message.reply_text(
        "👁 ICEGODS EchoEyes awakened.\n"
        "Use /check for instant balances.\n"
        "Auto reports every 4h, 8h, 12h, 24h, weekly, monthly.\n"
        "⚡ Now with instant balance change alerts!"
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = await build_report()
    save_log("Manual /check\n" + msg)
    await update.message.reply_text(msg)

# === Auto Reports ===
async def auto_report(app: Application, interval: str):
    msg = await build_report()
    save_log(f"⏰ {interval} Report\n" + msg)
    try:
        await app.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"⏰ {interval} Report\n\n{msg}")
    except:
        save_log("⚠️ Telegram send failed, log saved.")

# === Main ===
def main():
    request = HTTPXRequest(connect_timeout=30, read_timeout=30, write_timeout=30, pool_timeout=30)
    app = Application.builder().token(BOT_TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: asyncio.create_task(auto_report(app, "4h")), "interval", hours=4)
    scheduler.add_job(lambda: asyncio.create_task(auto_report(app, "8h")), "interval", hours=8)
    scheduler.add_job(lambda: asyncio.create_task(auto_report(app, "12h")), "interval", hours=12)
    scheduler.add_job(lambda: asyncio.create_task(auto_report(app, "24h")), "interval", hours=24)
    scheduler.add_job(lambda: asyncio.create_task(auto_report(app, "Weekly")), "interval", weeks=1)
    scheduler.add_job(lambda: asyncio.create_task(auto_report(app, "Monthly")), "interval", weeks=4)

    # 🔔 Balance change check every 2 minutes
    scheduler.add_job(lambda: asyncio.create_task(detect_changes(app)), "interval", minutes=2)

    scheduler.start()
    app.run_polling()

if __name__ == "__main__":
    main()
