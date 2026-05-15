from flask import Flask
import threading
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "8296488678:AAHo_wQ1pqbC6o3koT4MqWnmUrqTVV8t6xs"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Running"

def start(update, context):
    update.message.reply_text("هلا! البوت شغال")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))


updater.start_polling()
    
    updater.idle()

threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
