from flask import Flask
import threading
import yfinance as yf
from telegram.ext import Updater, CommandHandler

TOKEN = "8296488678:AAHo_wQ1pqbC6o3koT4MqWnmUrqTVV8t6xs"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

def start(update, context):
    update.message.reply_text("🚀 هلا! بوت EO Market شغال\nاكتب /signal")

def signal(update, context):
    update.message.reply_text("⏳ جاري تحليل EUR/USD و GBP/USD...")

    msg = "📊 تحليل حقيقي — فريم 5 دقائق\n\n"

    for symbol, name in [("EURUSD=X", "EUR/USD"), ("GBPUSD=X", "GBP/USD")]:
        data = yf.download(symbol, period="5d", interval="5m", progress=False)

        close = data["Close"]
        price = float(close.iloc[-1])
        ema200 = float(close.ewm(span=200).mean().iloc[-1])

        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rsi = float((100 - (100 / (1 + gain / loss))).iloc[-1])

        if price > ema200 and rsi > 55:
            decision = "شراء محتمل"
        elif price < ema200 and rsi < 45:
            decision = "بيع محتمل"
        else:
            decision = "انتظار"

        msg += f"""
{name}
السعر: {price:.5f}
EMA200: {ema200:.5f}
RSI: {rsi:.2f}
القرار: {decision}

━━━━━━━━━━━━
"""

    update.message.reply_text(msg)

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("signal", signal))

    updater.start_polling()
    updater.idle()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
