import re
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from payments import check_eth_payment, check_sol_payment

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to ICEGODS Payment Bot 💎\n\n"
        "Use /checketh <txhash> <amount> to verify ETH payment.\n"
        "Use /checksol <signature> <amount> to verify SOL payment."
    )

async def checketh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /checketh <txhash> <amount_eth>")
        return
    tx_hash, amount = context.args[0], float(context.args[1])
    status, msg = check_eth_payment(tx_hash, amount)
    await update.message.reply_text(msg)

async def checksol(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /checksol <signature> <amount_sol>")
        return
    signature, amount = context.args[0], float(context.args[1])
    status, msg = check_sol_payment(signature, amount)
    await update.message.reply_text(msg)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("checketh", checketh))
    app.add_handler(CommandHandler("checksol", checksol))
    app.run_polling()