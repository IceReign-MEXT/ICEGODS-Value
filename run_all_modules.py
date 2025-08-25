import subprocess

modules = [
    "EmailMonitor/email_monitor.py",
    "WalletMonitor/wallet_monitor.py",
    "SmartContractWatch/smart_contract_watch.py",
    "AutoRevoke/auto_revoke.py",   # ✅ added AutoRevoke
]

def start_modules():
    procs = []
    for module in modules:
        try:
            p = subprocess.Popen(["python", module])
            procs.append(p)
            print(f"✅ Started: {module}")
        except Exception as e:
            print(f"❌ Failed to start {module}: {e}")
    return procs

if __name__ == "__main__":
    print("✅ Modules started:", ", ".join(modules))
    procs = start_modules()
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down modules...")
        for p in procs:
            p.terminate()
