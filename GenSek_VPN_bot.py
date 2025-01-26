from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
import logging

# Создаем приложение Flask
app = Flask(__name__)

# Получаем токен из переменной окружения
token = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет, я твой бот!")

@app.route('/')
def index():
    return 'Бот работает!'

def main():
    # Используем Application вместо Updater
    application = Application.builder().token(token).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    # Запускаем Flask сервер
    from threading import Thread
    thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000))
    thread.start()
    
    # Запускаем polling для бота
    main()
