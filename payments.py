# payments.py
import requests
import os
from decimal import Decimal

USD_ETH_PRICE_API = "https://api.coinbase.com/v2/prices/ETH-USD/spot"
USD_SOL_PRICE_API = "https://api.coinbase.com/v2/prices/SOL-USD/spot"

def get_price_usd(symbol="ETH"):
    try:
        if symbol == "ETH":
            r = requests.get(USD_ETH_PRICE_API, timeout=10).json()
            return float(r["data"]["amount"])
        else:
            r = requests.get(USD_SOL_PRICE_API, timeout=10).json()
            return float(r["data"]["amount"])
    except Exception:
        return None

def verify_eth_tx(txhash, my_address, etherscan_api_key):
    """
    Verify that txhash sent funds to my_address.
    Returns (True, amount_usd) or (False, 0)
    """
    base = "https://api.etherscan.io/api"
    params = {"module":"proxy","action":"eth_getTransactionByHash","txhash":txhash}
    r = requests.get(base, params=params, timeout=10).json()
    tx = r.get("result")
    if not tx:
        return False, 0
    # to address
    to = tx.get("to")
    if not to:
        return False, 0
    if to.lower() != my_address.lower():
        # maybe it's to a contract; we could check logs but skip for now
        return False, 0
    value_hex = tx.get("value", "0x0")
    value = int(value_hex, 16) / (10**18)
    price = get_price_usd("ETH") or 0
    return True, float(value) * price

def verify_sol_tx(txhash, my_address, solana_rpc_url="https://api.mainnet-beta.solana.com"):
    """
    Verify a solana tx by signature. Get post balances or parsed inner instructions.
    Returns (True, amount_usd) or (False, 0)
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc":"2.0",
        "id":1,
        "method":"getConfirmedTransaction",
        "params":[txhash, "jsonParsed"]
    }
    r = requests.post(solana_rpc_url, json=payload, headers=headers, timeout=10).json()
    result = r.get("result")
    if not result:
        return False, 0
    # search for a native SOL transfer to my_address
    meta = result.get("meta", {})
    pre = meta.get("preBalances", [])
    post = meta.get("postBalances", [])
    # This is less reliable; instead search parsed instructions
    tx = result.get("transaction", {})
    message = tx.get("message", {})
    instructions = message.get("instructions", [])
    lamports = 0
    # Try to detect transfers
    for instr in instructions:
        parsed = instr.get("parsed")
        if not parsed:
            continue
        if parsed.get("type") == "transfer":
            info = parsed.get("info", {})
            dest = info.get("destination")
            if dest == my_address:
                amount = float(info.get("lamports")) / 1e9
                lamports += amount
    if lamports == 0:
        # fallback: compute from post-pre by matching account index; best-effort
        # skip for simplicity
        return False, 0
    price = get_price_usd("SOL") or 0
    return True, lamports * price