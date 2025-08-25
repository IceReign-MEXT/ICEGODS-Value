import os
import requests
import asyncio
from telegram import Bot

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def fetch_top_coins():
    url = "https://pro-api.coingecko.com/api/v3/coins/markets"
    headers = {"x-cg-pro-api-key": COINGECKO_API_KEY}
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        message = "💹 Top 20 Coins:\n"
        for coin in data:
            message += f"{coin['symbol'].upper()}: ${coin['current_price']:,}\n"
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ Failed to fetch prices: {e}")

async def whale_alerts():
    import random
    coins = ["BTC", "ETH", "SOL", "USDT"]
    coin = random.choice(coins)
    amount = round(random.uniform(50, 500), 2)
    usd_value = amount * random.randint(20000, 30000)
    message = f"🚨 🚨 🚨 Whale Alert!\n{amount} {coin} (${usd_value:,}) transferred to unknown wallet"
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

async def main_loop():
    while True:
        await fetch_top_coins()
        await whale_alerts()
        await asyncio.sleep(300)  # every 5 minutes

if __name__ == "__main__":
    asyncio.run(main_loop())
