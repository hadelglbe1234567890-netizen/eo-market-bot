from flask import Flask
import threading
import requests
from telegram.ext import Updater, CommandHandler

TOKEN = "8296488678:AAHo_wQ1pqbC6o3koT4MqWnmUrqTVV8t6xs"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

def get_prices(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5d&interval=5m"
    r = requests.get(url, timeout=10)
    data = r.json()["chart"]["result"][0]
    closes = data["indicators"]["quote"][0]["close"]
    closes = [c for c in closes if c is not None]
    return closes

def ema(values, period=200):
    k = 2 / (period + 1)
    e = values[0]
    for price in values[1:]:
        e = price * k + e * (1 - k)
    return e

def rsi(values, period=14):
    gains = []
    losses = []
    for i in range(1, len(values)):
        diff = values[i] - values[i - 1]
        gains.append(max(diff, 0))
        losses.append(abs(min(diff, 0)))

    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period

    if avg_loss == 0:
        return 100

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def analyze(symbol, name):
    prices = get_prices(symbol)

    if len(prices) < 200:
        return f"{name}\n❌ البيانات غير كافية الآن\n"

    price = prices[-1]
    ema200 = ema(prices[-200:], 200)
    rsi_now = rsi(prices)

    if price > ema200 and rsi_now > 55:
        decision = "شراء محتمل"
    elif price < ema200 and rsi_now < 45:
        decision = "بيع محتمل"
    else:
        decision = "انتظار"

    return f"""
{name}
السعر: {price:.5f}
EMA200: {ema200:.5f}
RSI: {rsi_now:.2f}
القرار: {decision}
"""

def start(update, context):
    update.message.reply_text("🚀 هلا! بوت EO Market شغال\nاكتب /signal")

def signal(update, context):
    update.message.reply_text("⏳ جاري تحليل EUR/USD و GBP/USD...")

    try:
        msg = "📊 تحليل حقيقي — فريم 5 دقائق\n\n"
        msg += analyze("EURUSD=X", "EUR/USD")
        msg += "\n━━━━━━━━━━━━\n"
        msg += analyze("GBPUSD=X", "GBP/USD")
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
