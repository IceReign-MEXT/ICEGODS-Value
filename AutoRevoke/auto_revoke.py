import asyncio
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.pubkey import Pubkey
from telegram import Bot
from telegram.error import TelegramError

# =======================
# CONFIG
# =======================
TELEGRAM_TOKEN = "8331786005:AAGPe1_OvFk8b-N49Plc69MiAGql81aY6yY"
CHAT_ID = "6453658778"
WALLETS = [
    "4tUTqBSzqz8eXbZPVdP2e5tiNRbFK3j5GFTqLEKubUzy",   # Solana wallet 1
    "G2uKjynRQs3GUTcCHGV7dyMsefvKskfMz1RakGEYMCBo"    # Solana wallet 2
]
RPC_URL = "https://api.mainnet-beta.solana.com"


# =======================
# CORE FUNCTIONS
# =======================

async def check_balances():
    """Check balance for all wallets and alert via Telegram"""
    bot = Bot(token=TELEGRAM_TOKEN)
    async with AsyncClient(RPC_URL, commitment=Confirmed) as client:
        for wallet in WALLETS:
            try:
                pubkey = Pubkey.from_string(wallet)
                balance_resp = await client.get_balance(pubkey)
                balance = balance_resp.value / 1e9  # lamports → SOL

                msg = f"📊 Wallet {wallet[:4]}...{wallet[-4:]} balance: {balance:.4f} SOL"
                await bot.send_message(chat_id=CHAT_ID, text=msg)

            except Exception as e:
                err_msg = f"⚠️ Error checking {wallet}: {str(e)}"
                try:
                    await bot.send_message(chat_id=CHAT_ID, text=err_msg)
                except TelegramError:
                    print(err_msg)


async def main_loop():
    """Keep running in background"""
    while True:
        await check_balances()
        await asyncio.sleep(60)  # check every 60 seconds


if __name__ == "__main__":
    asyncio.run(main_loop())
