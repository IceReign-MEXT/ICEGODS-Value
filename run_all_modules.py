import threading
import subprocess
import os

# =========================
# Environment Variables
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "8088"))
PAYMENT_PORT = int(os.getenv("PAYMENT_PORT", "5000"))

# =========================
# Helper Functions to Run Modules
# =========================

def run_wallet_monitor():
    try:
        import WalletMonitor
        WalletMonitor.run_monitor()
    except Exception as e:
        print(f"[WalletMonitor] Error: {e}")

def run_payment_webhook():
    try:
        subprocess.run(
            ["python3", "payment_webhook.py"],
            check=True
        )
    except Exception as e:
        print(f"[PaymentWebhook] Error: {e}")

def run_main_bot():
    try:
        subprocess.run(
            ["python3", "main.py"],
            check=True
        )
    except Exception as e:
        print(f"[MainBot] Error: {e}")

# =========================
# Start All Modules in Threads
# =========================
if __name__ == "__main__":
    threads = []

    # Wallet Monitor
    t_wallet = threading.Thread(target=run_wallet_monitor)
    threads.append(t_wallet)
    t_wallet.start()

    # Payment Webhook
    t_payment = threading.Thread(target=run_payment_webhook)
    threads.append(t_payment)
    t_payment.start()

    # Main Telegram Bot + Dashboard
    t_bot = threading.Thread(target=run_main_bot)
    threads.append(t_bot)
    t_bot.start()

    # Wait for all threads
    for t in threads:
        t.join()
