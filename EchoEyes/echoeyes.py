import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from web3 import Web3
import requests

# === Telegram Bot Token ===
TELEGRAM_TOKEN = "8331786005:AAGPe1_OvFk8b-N49Plc69MiAGql81aY6yY"

# === Wallets to Track ===
WALLETS = {
    "Bitcoin": "bc1qg6mvxr0taxv2x4fmwsg5y4rdf52tt0h45cqnvv",
    "Ethereum": "0x08D171685e51bAf7a929cE8945CF25b3D1Ac9756",
    "Solana": "3JqvK1ZAt67nipBVgZj6zWvuT8icMWBMWyu5AwYnhVss",
}

# === Solana Client ===
solana_client = AsyncClient("https://api.mainnet-beta.solana.com")

# === Ethereum Client ===
eth_client = Web3(Web3.HTTPProvider("https://eth.llamarpc.com"))

# === Price API ===
def get_price(symbol: str):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
        r = requests.get(url).json()
        return r[symbol]["usd"]
    except:
        return 0.0

# === Balance Functions ===
async def get_solana_balance(address):
    try:
        pubkey = Pubkey.from_string(address)
        balance = await solana_client.get_balance(pubkey)
        lamports = balance.value
        sol = lamports / 1_000_000_000
        return sol
    except:
        return 0.0

def get_eth_balance(address):
    try:
        balance = eth_client.eth.get_balance(address)
        return eth_client.from_wei(balance, "ether")
    except:
        return 0.0

def get_btc_balance(address):
    try:
        url = f"https://blockchain.info/q/addressbalance/{address}"
        r = requests.get(url).text
        satoshis = int(r)
        return satoshis / 100_000_000
    except:
        return 0.0

# === Telegram Command ===
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "👁 ICEGODS EchoEyes Balance Report 👁\n\n"

    # Solana
    sol_balance = await get_solana_balance(WALLETS["Solana"])
    sol_price = get_price("solana")
    message += f"💠 Solana {WALLETS['Solana'][:6]}...{WALLETS['Solana'][-4:]}: {sol_balance:.4f} SOL (${sol_balance * sol_price:.2f})\n"

    # Ethereum
    eth_balance = get_eth_balance(WALLETS["Ethereum"])
    eth_price = get_price("ethereum")
    message += f"⚡ Ethereum {WALLETS['Ethereum'][:6]}...{WALLETS['Ethereum'][-4:]}: {eth_balance:.4f} ETH (${eth_balance * eth_price:.2f})\n"

    # Bitcoin
    btc_balance = get_btc_balance(WALLETS["Bitcoin"])
    btc_price = get_price("bitcoin")
    message += f"₿ Bitcoin {WALLETS['Bitcoin'][:6]}...{WALLETS['Bitcoin'][-4:]}: {btc_balance:.4f} BTC (${btc_balance * btc_price:.2f})\n"

    await update.message.reply_text(message)

# === Main Bot ===
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("balance", balance))
    print("👁 ICEGODS EchoEyes is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
