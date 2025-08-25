# ICEGODS — iClose Box (Pro Bot + Dashboard)

## TL;DR
ICEGODS is an all-in-one **crypto intelligence and monetization box**:
- Telegram Pro Bot with **subscriptions**
- **Auto Whale Alerts** (BTC) and live prices (BTC, ETH, SOL, USDT)
- **Web Dashboard** with real-time charts
- Clean setup for creators to earn from their tools

---

## 1. Problem
Crypto signals and tools are scattered, unreliable, and hard to monetize. Most users give up before they find value.

## 2. Solution
**ICEGODS iClose Box** bundles everything:
- 🧠 Telegram bot users understand immediately
- 💳 One-click subscription flow with on-chain verification (expandable)
- 👀 Real-time market intelligence (whales + prices)
- 📊 A simple dashboard anyone can open

## 3. What the Box Does
- **Subscriptions**: users pick a plan and pay to your wallets.
- **Prices**: `/prices` (or `/prices all`) from Coingecko.
- **Whale Alerts**: automatic BTC high-value transfers in your channel.
- **Dashboard**: charts for BTC/ETH/SOL/USDT in a clean web page.

## 4. Plans & Pricing (example)
- **Basic** (30 days): 10 USDT / 0.05 SOL / 0.003 ETH / 0.00015 BTC  
- **Pro** (30 days): 25 USDT / 0.12 SOL / 0.007 ETH / 0.00035 BTC  
- **Elite** (30 days): 50 USDT / 0.25 SOL / 0.014 ETH / 0.0007 BTC

> Change prices anytime in `icegods_pro_bot.py` → `PLANS`.

## 5. Architecture
- **Telegram Bot**: `python-telegram-bot 21.x`
- **Prices**: Coingecko Simple Price API
- **Whales**: BTC unconfirmed pool + price conversion
- **Dashboard**: Flask + Chart.js (client fetch from Coingecko)
- **Storage**: SQLite (`subscriptions.db`)

## 6. Security & Privacy
- Keep your `.env` private.
- Wallets are your own; we do **not** custody funds.
- Add API keys later for more chains if needed.

## 7. Roadmap
- Add **ETH & SOL whale scanners**
- Web **admin panel** for subscribers and revenue
- Auto-renew & coupons
- On-chain proof-of-payment with amount+memo

## 8. Get Started
1. Fill `config.env` with your token & wallets  
2. `pip install ...` (see README)  
3. `bash start_masterbot.sh` & `bash start_dashboard.sh`  
4. Share your bot and dashboard
