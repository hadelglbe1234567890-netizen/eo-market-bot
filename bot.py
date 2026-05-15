from flask import Flask
import threading
import requests
from telegram.ext import Updater, CommandHandler

TOKEN = "8296488678:AAEE60UKeziTitmzGZzorxHffZcV9VZp7bY"
API_KEY = "‏b0feb8b1d8ba4db0ac256fb296f3c23d"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

def analyze(symbol, name):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "5min",
        "outputsize": "250",
        "apikey": API_KEY
    }

    data = requests.get(url, params=params, timeout=15).json()

    if "values" not in data:
        return f"{name}\n❌ خطأ من TwelveData:\n{data.get('message', data)}\n"

    closes = [float(x["close"]) for x in data["values"]]
    closes.reverse()

    price = closes[-1]
    avg = sum(closes[-20:]) / 20

    if price > avg:
        decision = "شراء 🟢"
    else:
        decision = "بيع 🔴"

    return f"""
📊 {name}

💰 السعر الحالي: {price:.5f}
📈 متوسط 20 شمعة: {avg:.5f}
📌 القرار: {decision}
⏳ الفريم: 5 دقائق
"""

def start(update, context):
    update.message.reply_text("🚀 هلا! بوت EO Market شغال\nاكتب /signal")

def signal(update, context):
    update.message.reply_text("⏳ جاري تحليل EUR/USD و GBP/USD...")

    msg = "📊 تحليل حقيقي — فريم 5 دقائق\n\n"
    msg += analyze("EUR/USD", "EUR/USD")
    msg += "\n━━━━━━━━━━━━\n"
    msg += analyze("GBP/USD", "GBP/USD")

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
