from flask import Flask
import threading
import requests
from telegram.ext import Updater, CommandHandler

TOKEN = "8296488678:AAGX93yKew0WSgGZrLKAANvC1LJCbcYBpQ8"
API_KEY = "‏b0feb8b1d8ba4db0ac256fb296f3c23d"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

def analyze(symbol):

    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=5min&outputsize=50&apikey={API_KEY}"

    r = requests.get(url)
    data = r.json()

    closes = [float(x["close"]) for x in data["values"]]

    price = closes[0]
    avg = sum(closes[:20]) / 20

    if price > avg:
        decision = "شراء 🟢"
    else:
        decision = "بيع 🔴"

    return f"""
📊 {symbol}

💰 السعر الحالي: {price}
📈 المتوسط: {round(avg,5)}

📌 القرار: {decision}
⏳ الفريم: 5 دقائق
"""

def start(update, context):
    update.message.reply_text("🚀 هلا! بوت EO Market شغال\nاكتب /signal")

def signal(update, context):

    update.message.reply_text("⏳ جاري تحليل EUR/USD و GBP/USD...")

    try:

        msg = "📊 تحليل حقيقي — فريم 5 دقائق\n"

        msg += analyze("EUR/USD")
        msg += "\n━━━━━━━━━━━━\n"
        msg += analyze("GBP/USD")

        update.message.reply_text(msg)

    except Exception as e:
        update.message.reply_text(f"❌ خطأ أثناء التحليل:\n{e}")

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
