#!/usr/bin/env python3
# SmartContractWatch — Solana opportunities monitor (no auto-spend)
# - Alerts: governance activity, staking APR pings, farm notices, (optional) airdrop checks
# - Safe: read-only; you decide actions manually.

import os, time, json, pathlib, requests

# === Config (from ~/MasterBot/config.env via runner) ===
TOKEN = os.getenv("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
SOLANA_WALLETS = [w.strip() for w in os.getenv("SOLANA_WALLETS", "").split(",") if w.strip()]
INTERVAL = int(os.getenv("SCW_INTERVAL_SECONDS", "1800"))  # default 30 min

# Public Solana RPC
SOL_RPC = os.getenv("SOL_RPC", "https://api.mainnet-beta.solana.com")

# Known programs (examples; adjust later)
WATCH_PROGRAMS = {
    "Governance": "Gov111111111111111111111111111111111111111",     # Placeholder
    "Marinade Staking": "MarBmsSgVuxyNN9HGWcLxUDdQHXCEVvjX6zkqfr7fQD",
    "Lido Staking":     "CrX7kMhL7S6zXXHbFjZqQTFeRW9d2TPms6ybq9qsYbKE",
    "Raydium AMM":      "RVKd61ztZW9mHjnwkkpMdpWY6QecqDUnT7crYvXRkAJ",
}

# State persistence (to avoid duplicate alerts)
MODULE_DIR = pathlib.Path(__file__).resolve().parent
STATE_PATH = MODULE_DIR / ".state.json"

def load_state():
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {"governance_last_sig": None}

def save_state(state):
    try:
        STATE_PATH.write_text(json.dumps(state))
    except Exception as e:
        print(f"[SCW] State save error: {e}")

def send(msg: str):
    """Send Telegram alert or print fallback."""
    if not TOKEN or not CHAT_ID:
        print(f"[SCW] {msg}")
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=15
        )
    except Exception as e:
        print(f"[SCW] Telegram send error: {e}")

def sol_rpc(method, params):
    try:
        r = requests.post(
            SOL_RPC,
            json={"jsonrpc":"2.0","id":1,"method":method,"params":params},
            timeout=20
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise RuntimeError(f"RPC {method} failed: {e}")

def check_governance_activity(state):
    """Ping newest governance signature to detect fresh proposals/votes (placeholder program id)."""
    gov_pid = WATCH_PROGRAMS["Governance"]
    j = sol_rpc("getSignaturesForAddress", [gov_pid, {"limit": 1}])
    res = j.get("result") or []
    if not res:
        return state
    latest = res[0]
    latest_sig = latest.get("signature")
    if latest_sig and latest_sig != state.get("governance_last_sig"):
        slot = latest.get("slot")
        conf = latest.get("confirmationStatus", "unknown")
        send(
            "🗳 New governance activity detected\n"
            f"Program: Governance\n"
            f"Slot: {slot} | Conf: {conf}\n"
            f"Sig: {latest_sig}\n"
            f"View: https://solscan.io/tx/{latest_sig}"
        )
        state["governance_last_sig"] = latest_sig
    return state

def ping_staking_apr():
    """Static APR pings (replace with live sources later)."""
    aprs = {
        "Marinade": "7.3%",
        "Lido": "6.9%",
    }
    for name, apr in aprs.items():
        send(f"📈 {name} staking APR ping: {apr}\nConsider manual stake/unstake.")

def raydium_farm_notice():
    """Placeholder farm alert (manual)."""
    send("💎 Raydium farms: new/active pools may offer ~20–30% APR.\nBrowse: https://raydium.io/farms")

def airdrop_check(wallet: str):
    """Placeholder airdrop scan (indexers/APIs can be integrated later)."""
    # Return None or a brief string describing potential claim
    return None

def run_cycle():
    state = load_state()
    # Governance
    try:
        state = check_governance_activity(state)
    except Exception as e:
        send(f"⚠️ Governance check failed: {e}")

    # Staking APR pings
    try:
        ping_staking_apr()
    except Exception as e:
        send(f"⚠️ Staking APR ping failed: {e}")

    # Raydium farms
    try:
        raydium_farm_notice()
    except Exception as e:
        send(f"⚠️ Farm notice failed: {e}")

    # Airdrops per wallet
    for w in SOLANA_WALLETS:
        try:
            found = airdrop_check(w)
            if found:
                send(f"🎁 Airdrop opportunity for {w}: {found}")
        except Exception as e:
            send(f"⚠️ Airdrop check failed for {w}: {e}")

    save_state(state)

def main():
    send("🟣 SmartContractWatch started (read-only opportunities; no auto-spend).")
    if not SOLANA_WALLETS:
        send("ℹ️ No SOLANA_WALLETS set in config.env.")
    while True:
        try:
            run_cycle()
        except Exception as e:
            send(f"🔴 SCW cycle error: {e}")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
