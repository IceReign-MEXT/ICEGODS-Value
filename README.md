# MasterBot (Termux)

Clean skeleton ready for your modules. Paste your code into the files below.

## Structure
- `run_all_modules.py` — Master runner (you paste your final runner here)
- `config.env` — Global config (Telegram/Wallets/Emails, etc.)
- `WalletMonitor/` — Paste `wallet_monitor.py` here
- `EmailMonitor/` — Paste `email_monitor.py` here
- `BotModule1/` — Paste your custom `bot1.py` here
- `BotModule2/` — Paste your custom `bot2.py` here
- `SmartContractWatch/` — Paste `smart_contract_watch.py` here
- `docs/` — Banner, Roadmap, Whitepaper draft

## Usage
1. Edit `config.env` (uncomment & set your values).
2. Paste your module code into each folder.
3. Paste your master runner into `run_all_modules.py`.
4. Run: `cd ~/MasterBot && python run_all_modules.py`
