import json, os
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

SUB_FILE = os.path.expanduser("~/MasterBot/subscriptions.json")

def load_subs():
    if os.path.exists(SUB_FILE):
        with open(SUB_FILE) as f:
            return json.load(f)
    return {}

def save_subs(data):
    with open(SUB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def subscribe(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    if len(context.args) == 0:
        update.message.reply_text("Usage: /subscribe <plan>\nPlans: free, pro, vip")
        return
    plan = context.args[0].lower()
    subs = load_subs()
    subs[chat_id] = {"plan": plan, "expires": "pending"}
    save_subs(subs)
    update.message.reply_text(
        f"💳 You selected *{plan}* plan.\n\n"
        "Send payment to one of the deposit wallets:\n"
        "• SOL: 4tUTqBSzqz8eXbZPVdP2e5tiNRbFK3j5GFTqLEKubUzy\n"
        "• ETH: 0x1650dcf7c462cb101c6b399b2deeceb72d09af6f\n"
        "• BTC: bc1qe8pf5nzj553kcyv0nl4p5cl6edrsl8ullffkmk\n\n"
        "After payment, wait for admin to confirm. ✅"
    )

def confirm(update: Update, context: CallbackContext):
    admin_id = "6453658778"  # replace with your Telegram ID
    if str(update.effective_chat.id) != admin_id:
        update.message.reply_text("❌ Only admin can confirm payments.")
        return
    if len(context.args) < 3:
        update.message.reply_text("Usage: /confirm <user_id> <plan> <expiry YYYY-MM-DD>")
        return
    user_id, plan, expiry = context.args[0], context.args[1], context.args[2]
    subs = load_subs()
    subs[user_id] = {"plan": plan, "expires": expiry}
    save_subs(subs)
    update.message.reply_text(f"✅ Subscription updated for user {user_id} → {plan} until {expiry}")

def status(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    subs = load_subs()
    if chat_id in subs:
        plan = subs[chat_id]["plan"]
        expires = subs[chat_id]["expires"]
        update.message.reply_text(f"📊 Plan: {plan}\n⏳ Expires: {expires}")
    else:
        update.message.reply_text("❌ No subscription found. Use /subscribe <plan> to begin.")

# Register handlers
updater.dispatcher.add_handler(CommandHandler("subscribe", subscribe))
updater.dispatcher.add_handler(CommandHandler("confirm", confirm))
updater.dispatcher.add_handler(CommandHandler("status", status))
