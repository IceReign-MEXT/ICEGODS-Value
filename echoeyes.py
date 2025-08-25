async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Deposit wallets:\n"
        "Bitcoin (BTC): bc1qes8kuftes4axt76a73xv48770m9fzherf3ld53\n"
        "Bitcoin (BTC legacy): 3JqvK1ZAt67nipBVgZj6zWvuT8icMWBMWyu5AwYnhVss\n"
        "Ethereum (ETH): 0x08D171685e51bAf7a929cE8945CF25b3D1Ac9756"
    )
