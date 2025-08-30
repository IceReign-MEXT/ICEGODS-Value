import os
import time
from web3 import Web3
from solana.rpc.api import Client as SolanaClient
from dotenv import load_dotenv
from telegram import Bot

# =========================
# Load Environment Variables
# =========================
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

SOLANA_WALLETS = os.getenv("SOLANA_WALLETS")
ETH_WALLET = os.getenv("ETH_WALLET")
BTC_WALLET = os.getenv("BTC_WALLET")
USDT_WALLET = os.getenv("USDT_WALLET")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# =========================
# Initialize Clients
# =========================
sol_client = SolanaClient("https://api.mainnet-beta.solana.com")
eth_client = Web3(Web3.HTTPProvider(os.getenv("INFURA_MAINNET")))

# =========================
# Wallet Monitoring Logic
# =========================
def check_solana_balance():
    balances = {}
    for wallet in SOLANA_WALLETS.split(","):
        resp = sol_client.get_balance(wallet)
        if resp.get("result"):
            balances[wallet] = resp["result"]["value"] / 1e9
    return balances
