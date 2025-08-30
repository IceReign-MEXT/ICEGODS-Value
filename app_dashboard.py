from flask import Flask, render_template_string
import requests, os
from dotenv import load_dotenv

# Load .env
load_dotenv(os.path.expanduser("~/MasterBot/config.env"))

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
TOP_N = int(os.getenv("COINGECKO_TOP_N", 100))
SOL_ADDR = os.getenv("WALLET_SOL")
ETH_ADDR = os.getenv("WALLET_ETH")
BTC_ADDR = os.getenv("WALLET_BTC")

PLANS = {
    "basic": {"duration_days": 30, "prices": {"USDT": 10, "SOL": 0.05, "ETH": 0.003, "BTC": 0.00015}},
    "pro": {"duration_days": 30, "prices": {"USDT": 25, "SOL": 0.12, "ETH": 0.007, "BTC": 0.00035}},
    "elite": {"duration_days": 30, "prices": {"USDT": 50, "SOL": 0.25, "ETH": 0.014, "BTC": 0.0007}},
}

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>ICEGODS Dashboard</title>
<style>
body { font-family: Arial, sans-serif; background: #0b0c10; color: #c5c6c7; }
h1 { color: #66fcf1; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: 8px; text-align: left; border-bottom: 1px solid #45a29e; }
th { color: #66fcf1; }
tr:hover {background-color:#1f2833;}
.wallet, .plans { margin-top:20px; }
</style>
</head>
<body>
<h1>ICEGODS Dashboard</h1>
<h2>Top {{coins|length}} Coins</h2>
<table>
<tr><th>Symbol</th><th>Name</th><th>Price USD</th><th>Market Cap</th></tr>
{% for c in coins %}
<tr>
<td>{{c.symbol.upper()}}</td>
<td>{{c.name}}</td>
<td>${{c.current_price:,.2f}}</td>
<td>${{c.market_cap:,.0f}}</td>
</tr>
{% endfor %}
</table>

<div class="plans">
<h2>Subscription Plans</h2>
<ul>
{% for p, info in plans.items() %}
<li><b>{{p.capitalize()}} ({{info.duration_days}} days):</b> {{info.prices.USDT}} USDT / {{info.prices.SOL}} SOL / {{info.prices.ETH}} ETH / {{info.prices.BTC}} BTC</li>
{% endfor %}
</ul>
</div>

<div class="wallet">
<h2>Deposit Wallets</h2>
<ul>
<li>SOL: {{wallets.SOL}}</li>
<li>ETH: {{wallets.ETH}}</li>
<li>BTC: {{wallets.BTC}}</li>
</ul>
</div>
</body>
</html>
"""

@app.route("/")
def index():
    try:
        r = requests.get(f"https://pro-api.coingecko.com/api/v3/coins/markets",
                         headers={"x-cg-pro-api-key": COINGECKO_API_KEY},
                         params={"vs_currency": "usd","order":"market_cap_desc","per_page": TOP_N,"page":1})
        coins = r.json()
    except:
        coins = []
    return render_template_string(TEMPLATE, coins=coins, plans=PLANS, wallets={"SOL":SOL_ADDR,"ETH":ETH_ADDR,"BTC":BTC_ADDR})

if __name__ == "__main__":
    port = int(os.getenv("DASHBOARD_PORT", 8088))
    app.run(host="0.0.0.0", port=port)
