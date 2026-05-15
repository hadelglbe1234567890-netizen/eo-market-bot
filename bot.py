from flask import Flask
import threading
import yfinance as yf
import pandas as pd
from telegram.ext import Updater, CommandHandler

TOKEN = "8296488678:AAHo_wQ1pqbC6o3koT4MqWnmUrqTVV8t6xs"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = -delta.where(delta < 0, 0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def analyze(symbol):
    data = yf.download(symbol, period="5d", interval="5m", progress=False)

    if data.empty:
        return f"{symbol}: ما قدرت أجيب البيانات."

    close = data["Close"]
    high = data["High"]
    low = data["Low"]

    ema200 = close.ewm(span=200).mean().iloc[-1]
    rsi_now = rsi(close).iloc[-1]
    price = close.iloc[-1]

    if price > ema200 and rsi_now > 55:
        decision = "شراء محتمل"
    elif price < ema200 and rsi_now < 45:
        decision = "بيع محتمل"
    else:
        decision = "انتظار"

    return f"""
{symbol}
السعر: {price:.5f}
EMA200: {ema200:.5f}
RSI: {rsi_now:.2f}
القرار: {decision}
"""

def start(update, context):
    update.message.reply_text("هلا! بوت EO Market شغال 🚀\nاكتب /signal")

def signal(update, context):
    msg = "📊 تحليل حقيقي — فريم 5 دقائق\n\n"
    msg += analyze("EURUSD=X")
    msg += "\n━━━━━━━━━━━━\n"
    msg += analyze("GBPUSD=X")
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
