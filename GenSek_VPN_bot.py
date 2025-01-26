from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher
import os

app = Flask(__name__)

# Получаем токен из переменной окружения
token = os.getenv('TELEGRAM_TOKEN')

# Создаем объект бота
bot = Bot(token)

# Инициализируем диспетчер
dispatcher = Dispatcher(bot, None, workers=0)

# Обработчик команды /start
def start(update, context):
    update.message.reply_text("Привет, я твой бот!")

# Регистрируем обработчик команды /start
dispatcher.add_handler(CommandHandler("start", start))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Получаем обновления от Telegram
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, bot)
    dispatcher.process_update(update)
    return "OK"

if __name__ == '__main__':
    # Устанавливаем webhook
    webhook_url = os.getenv('WEBHOOK_URL')  # Например, URL твоего приложения на Render
    bot.set_webhook(url=webhook_url + '/webhook')

    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
