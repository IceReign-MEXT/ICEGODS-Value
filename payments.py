import requests
import os

ETH_ADDRESS = os.getenv("ETH_ADDRESS")
SOL_ADDRESS = os.getenv("SOL_ADDRESS")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
SOLANA_RPC = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")

def check_eth_payment(tx_hash, amount_eth):
    url = f"https://api.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash={tx_hash}&apikey={ETHERSCAN_API_KEY}"
    tx_status = requests.get(url).json()
    
    if tx_status.get("status") != "1":
        return False, "Transaction not confirmed."

    tx_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={ETH_ADDRESS}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    txs = requests.get(tx_url).json()

    for tx in txs.get("result", []):
        if tx["hash"].lower() == tx_hash.lower() and float(tx["value"]) / 1e18 >= amount_eth:
            return True, "Payment confirmed."
    return False, "Payment not found."

def check_sol_payment(tx_signature, amount_sol):
    headers = {"Content-Type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedTransaction",
        "params": [tx_signature, "json"]
    }
    r = requests.post(SOLANA_RPC, headers=headers, json=payload).json()
    if not r.get("result"):
        return False, "Transaction not confirmed."

    # Check if correct destination and amount
    try:
        instructions = r["result"]["transaction"]["message"]["instructions"]
        for ix in instructions:
            if SOL_ADDRESS in str(ix) and str(amount_sol) in str(ix):
                return True, "Payment confirmed."
    except:
        return False, "Error reading transaction."
    
    return False, "Payment not found."