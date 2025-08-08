import time
import json
import threading
from ghost_core import GhostCore
from eth_watcher import EthereumWatcher
from sol_watcher import SolanaWatcher
from telegram_alerts import TelegramNotifier

# Load config
with open("config.json") as f:
    config = json.load(f)

# INIT modules
core = GhostCore(config)
tg = TelegramNotifier(config["telegram_token"], config["telegram_chat_id"])
eth = EthereumWatcher(config, core, tg)
sol = SolanaWatcher(config, core, tg)

def start_eth_watcher():
    while True:
        try:
            eth.monitor_wallets()
        except Exception as e:
            tg.send_alert(f"[ETH Error] {str(e)}")
            time.sleep(2)

def start_sol_watcher():
    while True:
        try:
            sol.monitor_wallets()
        except Exception as e:
            tg.send_alert(f"[SOL Error] {str(e)}")
            time.sleep(2)

if __name__ == '__main__':
    tg.send_alert("🚨 GhostMex is now LIVE and monitoring wallets!")

    eth_thread = threading.Thread(target=start_eth_watcher)
    sol_thread = threading.Thread(target=start_sol_watcher)

    eth_thread.start()
    sol_thread.start()

    eth_thread.join()
    sol_thread.join()