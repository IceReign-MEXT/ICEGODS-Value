#!/usr/bin/env python3
"""
RevokeMonitor — scans ERC20 allowances for monitored Ethereum address(es)
and alerts via Telegram when a spender has a non-zero allowance.

- Read-only by default: no private key, no transactions sent.
- It can also build an unsigned "revoke" transaction payload (for manual signing).
- To enable automatic sending of revoke txs you must explicitly opt-in and run
  the revoke-sender script on a secure machine (I can provide that separately).
"""

import os, time, json, requests
from web3 import Web3
from eth_utils import to_checksum_address

# --- CONFIG: set in ~/MasterBot/config.env or export in environment ---
INFURA = os.getenv("ETH_NODE_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_ID")
MONITOR_ADDR = os.getenv("MONITOR_ETH_ADDRESS", "").strip()  # e.g. 0x...
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

# comma-separated token list and spender list in config.env (optional)
TOKENS = [t.strip() for t in os.getenv("MONITOR_TOKENS", "").split(",") if t.strip()]
SPENDERS = [s.strip() for s in os.getenv("MONITOR_SPENDERS", "").split(",") if s.strip()]

# Minimal ERC20 ABI for allowance() and decimals() and symbol()
ERC20_MIN_ABI = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"}]')

w3 = Web3(Web3.HTTPProvider(INFURA, request_kwargs={"timeout": 15}))

STATE_FILE = os.path.join(os.path.dirname(__file__), ".revoke_state.json")

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_state(s):
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(s, f)
    except Exception as e:
        print("state save error", e)

def send_telegram(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("(tg disabled)", msg)
        return
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                      data={"chat_id": TELEGRAM_CHAT_ID, "text": msg}, timeout=10)
    except Exception as e:
        print("tg send failed", e)

def check_allowance(token_addr, spender, owner):
    try:
        token = w3.eth.contract(address=to_checksum_address(token_addr), abi=ERC20_MIN_ABI)
        allowance = token.functions.allowance(to_checksum_address(owner), to_checksum_address(spender)).call()
        decimals = token.functions.decimals().call()
        symbol = token.functions.symbol().call()
        amount = allowance / (10 ** decimals)
        return {"symbol": symbol, "amount": amount, "raw": allowance}
    except Exception as e:
        return {"error": str(e)}

def build_revoke_payload(token_addr, spender, owner, nonce=None, gas=100000, gasPriceGwei=20):
    """Return an unsigned transaction dict that approves 0 (revoke). Manual signing required."""
    token = w3.eth.contract(address=to_checksum_address(token_addr), abi=ERC20_MIN_ABI)
    tx = token.functions.allowance(to_checksum_address(owner), to_checksum_address(spender)).buildTransaction({
        "from": to_checksum_address(owner),
        # nonce, gas, gasPrice to be filled by caller or after fetching network values
    })
    # Instead of building via allowance (which is read-only), build approve(0)
    # Minimal approve ABI piece:
    approve_fn = token.functions.approve(to_checksum_address(spender), 0)
    tx2 = approve_fn.buildTransaction({
        "from": to_checksum_address(owner),
    })
    return tx2

def main_loop(pause_seconds=60):
    if not MONITOR_ADDR:
        print("No MONITOR_ETH_ADDRESS set in config.env. Exiting.")
        return

    tokens = TOKENS[:]  # snapshot
    spenders = SPENDERS[:]

    state = load_state()
    state.setdefault("seen", {})

    send_telegram(f"🔎 RevokeMonitor started for {MONITOR_ADDR}. Tokens: {len(tokens)} Spenders: {len(spenders)}")

    while True:
        try:
            # if no token list provided, we try a small default set (common tokens) — safe fallback
            if not tokens:
                tokens = [
                    # these are placeholders; better to set MONITOR_TOKENS in config.env
                ]

            if not spenders:
                spenders = [
                    # placeholders; set MONITOR_SPENDERS in config.env for best results
                ]

            for t in tokens:
                for s in spenders:
                    res = check_allowance(t, s, MONITOR_ADDR)
                    if "error" in res:
                        print("check error", res["error"])
                        continue
                    key = f"{t.lower()}_{s.lower()}"
                    prev_amount = state["seen"].get(key, 0)
                    if res["amount"] > 0 and res["amount"] != prev_amount:
                        # new or changed non-zero allowance
                        msg = (f"🚨 Approval detected\nOwner: {MONITOR_ADDR}\nToken: {res['symbol']} ({t})\n"
                               f"Spender: {s}\nAllowance: {res['amount']}\n\n"
                               "Action: Revoke to 0. You can build unsigned tx by calling build_revoke_payload().")
                        send_telegram(msg)
                        state["seen"][key] = res["amount"]
                    elif res["amount"] == 0 and prev_amount != 0:
                        # allowance became zero
                        send_telegram(f"✅ Allowance cleared for token {res.get('symbol')} -> spender {s}")
                        state["seen"][key] = 0
            save_state(state)

        except Exception as e:
            send_telegram(f"RevokeMonitor error: {e}")
        time.sleep(pause_seconds)

if __name__ == "__main__":
    main_loop()
