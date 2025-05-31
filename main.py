import os
import time
from flask import Flask, request
import telebot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL")

if not API_TOKEN or not WEBHOOK_BASE_URL:
    raise RuntimeError("Missing TELEGRAM_API_TOKEN or WEBHOOK_BASE_URL.")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def handle_start(message):
    print(f"🟢 /start from {message.chat.id}")
    bot.send_photo(message.chat.id, photo='https://i.postimg.cc/nV0KwdBC/DALL-E-2024-05-04-20-46.jpg')
    bot.send_message(message.chat.id, 
        "🎉 Welcome to KWGGAME 🎉\n\n"
        "💸 Claim your rewards now!\n"
        "🌐 Visit: www.kwggame.com\n"
        "👉 Tap /menu to see options")

@bot.message_handler(commands=['menu'])
def handle_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🎁 Claim Bonus', '🎮 Play Games')
    markup.row('📞 Contact Support')
    bot.send_message(message.chat.id, "Please choose an option below:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    print(f"📩 Message from {message.chat.id}: {message.text}")

@app.route("/", methods=["GET"])
def index():
    return "KWGGAME Telegram Bot is running."

@app.route("/", methods=["POST"])
def webhook():
    raw = request.stream.read().decode("utf-8")
    print("📥 Incoming Webhook Data:", raw)
    update = telebot.types.Update.de_json(raw)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    try:
        print("🔄 Forcing webhook reset...")
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=f"{WEBHOOK_BASE_URL}/")
        print(f"✅ Webhook forcibly set to: {WEBHOOK_BASE_URL}/")
    except Exception as e:
        print(f"❌ Webhook error: {e}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))