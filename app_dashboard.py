#!/usr/bin/env python3
from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv('./config/config.env')

app = Flask(__name__, template_folder="templates")

# =====================
# Dashboard Routes
# =====================

@app.route("/")
def index():
    try:
        db_path = os.path.join(os.path.dirname(__file__), "subscriptions.db")
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT telegram_id, subscription FROM subscriptions")
        users = c.fetchall()
        conn.close()
    except Exception as e:
        users = []
        print(f"[Dashboard] Error fetching users: {e}")

    # Render safely, avoid syntax errors
    return render_template("index.html", users=users)

@app.route("/stats")
def stats():
    return "<h2>Dashboard Stats Placeholder</h2>"

@app.route("/webhook_test", methods=["POST"])
def webhook_test():
    data = request.get_json()
    print(f"[Dashboard] Webhook received: {data}")
    return {"status": "ok"}, 200

if __name__ == "__main__":
    # Debug=True will show errors in terminal for easier fixing
    app.run(host=os.getenv("DASHBOARD_HOST", "0.0.0.0"), 
            port=int(os.getenv("DASHBOARD_PORT", 8088)), 
            debug=True)
