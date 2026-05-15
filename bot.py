from flask import Flask
import threading
from telegram.ext import Updater, CommandHandler

TOKEN = "8296488678:AAHo_wQ1pqbC6o3koT4MqWnmUrqTVV8t6xs"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

def choose_duration(adx, rsi):
    if adx >= 30 and 45 <= rsi <= 65:
        return "10 دقائق"
    elif adx >= 25:
        return "5 دقائق"
    else:
        return "2-3 دقائق"

def start(update, context):
    update.message.reply_text("هلا! بوت EO Market شغال 🚀\nاكتب /signal")

def signal(update, context):
    msg = """
📊 تحليل الأسواق — فريم 5 دقائق

1️⃣ EUR/USD
💰 نسبة الربح: 83%
📌 القرار: انتظر
⏳ مدة الصفقة: لا تدخل الآن

السبب:
- السعر قريب من EMA200
- RSI قريب من التشبع
- ننتظر تأكيد أوضح

━━━━━━━━━━━━

2️⃣ GBP/USD
💰 نسبة الربح: 84%
📌 القرار: بيع محتمل
⏳ مدة الصفقة المقترحة: 5 دقائق

السبب:
- الاتجاه العام هابط
- إذا السعر تحت EMA200
- و RSI أقل من 45
- و ADX فوق 25
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
