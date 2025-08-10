#!/usr/bin/env python3
# ICEGODS — simple payment-check & balance bot (TeleBot version)

import os
import requests
from dotenv import load_dotenv
import telebot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ETH_ADDRESS = os.getenv("ETH_ADDRESS")
SOL_ADDRESS = os.getenv("SOL_ADDRESS")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")  # recommended
SOLANA_RPC = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")

if not BOT_TOKEN:
    print("ERROR: BOT_TOKEN not set in .env. Exiting.")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

def get_eth_balance(addr):
    if not ETHERSCAN_API_KEY:
        return "Etherscan API key missing (set ETHERSCAN_API_KEY)."
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest&apikey={ETHERSCAN_API_KEY}"
    r = requests.get(url, timeout=10).json()
    if r.get("status") == "1":
        wei = int(r["result"])
        return f"{wei/1e18:.6f} ETH"
    return "Unable to fetch ETH balance."

def get_sol_balance(addr):
    payload = {"jsonrpc":"2.0","id":1,"method":"getBalance","params":[addr, {"commitment":"finalized"}]}
    r = requests.post(SOLANA_RPC, json=payload, timeout=10).json()
    try:
        lamports = r["result"]["value"]
        return f"{lamports/1e9:.6f} SOL"
    except:
        return "Unable to fetch SOL balance."

def verify_eth_tx(txhash, min_amount_eth):
    if not ETHERSCAN_API_KEY:
        return False, "Etherscan API key missing."
    url = f"https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={txhash}&apikey={ETHERSCAN_API_KEY}"
    r = requests.get(url, timeout=10).json()
    tx = r.get("result")
    if not tx:
        return False, "Transaction not found or not yet indexed."
    to_addr = tx.get("to")
    value_hex = tx.get("value", "0x0")
    value_wei = int(value_hex, 16)
    value_eth = value_wei / 1e18
    if to_addr and ETH_ADDRESS and to_addr.lower() == ETH_ADDRESS.lower() and value_eth >= float(min_amount_eth):
        return True, f"Confirmed: received {value_eth:.6f} ETH to {to_addr}"
    return False, f"Not matched: to={to_addr} value={value_eth:.6f} ETH"

def verify_sol_tx(signature, min_amount_sol):
    payload = {"jsonrpc":"2.0","id":1,"method":"getTransaction","params":[signature, "jsonParsed"]}
    r = requests.post(SOLANA_RPC, json=payload, timeout=10).json()
    result = r.get("result")
    if not result:
        return False, "Transaction not found or not confirmed."
    try:
        message = result["transaction"]["message"]
        keys = [k["pubkey"] for k in message["accountKeys"]]
        meta = result.get("meta", {})
        preBalances = meta.get("preBalances", [])
        postBalances = meta.get("postBalances", [])
        if SOL_ADDRESS in keys:
            idx = keys.index(SOL_ADDRESS)
            pre = preBalances[idx]
            post = postBalances[idx]
            delta = post - pre
            sol_received = delta / 1e9
            if sol_received >= float(min_amount_sol):
                return True, f"Confirmed: received {sol_received:.6f} SOL"
            else:
                return False, f"Found but amount {sol_received:.6f} SOL less than required {min_amount_sol}"
        else:
            return False, "Target Solana address not involved in this tx."
    except Exception as e:
        return False, f"Error parsing Solana tx: {str(e)}"

# Commands
@bot.message_handler(commands=['start'])
def cmd_start(msg):
    bot.send_message(msg.chat.id,
        "👋 ICEGODS Value Bot\n\n"
        "Commands:\n"
        "/wallet - show tracked wallet balances\n"
        "/pay - show payment addresses\n"
        "/verify_eth <txhash> <amount_eth> - verify ETH payment\n"
        "/verify_sol <signature> <amount_sol> - verify SOL payment\n"
    )

@bot.message_handler(commands=['wallet'])
def cmd_wallet(msg):
    eth_b = get_eth_balance(ETH_ADDRESS) if ETH_ADDRESS else "ETH address not set."
    sol_b = get_sol_balance(SOL_ADDRESS) if SOL_ADDRESS else "SOL address not set."
    bot.send_message(msg.chat.id, f"🔎 Balances:\nETH: {eth_b}\nSOL: {sol_b}")

@bot.message_handler(commands=['pay'])
def cmd_pay(msg):
    reply = []
    if SOL_ADDRESS: reply.append(f"🔵 Solana: `{SOL_ADDRESS}`")
    if ETH_ADDRESS: reply.append(f"🟠 Ethereum: `{ETH_ADDRESS}`")
    if not reply:
        bot.send_message(msg.chat.id, "No payment addresses configured.")
    else:
        bot.send_message(msg.chat.id, "💸 Send payments to:\n" + "\n".join(reply))

@bot.message_handler(commands=['verify_eth'])
def cmd_verify_eth(msg):
    args = msg.text.split()
    if len(args) < 3:
        bot.send_message(msg.chat.id, "Usage: /verify_eth <txhash> <amount_eth>")
        return
    tx, amount = args[1], args[2]
    ok, text = verify_eth_tx(tx, amount)
    bot.send_message(msg.chat.id, ("✅ " if ok else "❌ ") + text)

@bot.message_handler(commands=['verify_sol'])
def cmd_verify_sol(msg):
    args = msg.text.split()
    if len(args) < 3:
        bot.send_message(msg.chat.id, "Usage: /verify_sol <signature> <amount_sol>")
        return
    sig, amount = args[1], args[2]
    ok, text = verify_sol_tx(sig, amount)
    bot.send_message(msg.chat.id, ("✅ " if ok else "❌ ") + text)

if __name__ == "__main__":
    print("ICEGODS Value Bot starting...")
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print("Bot crashed:", e)