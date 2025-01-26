from telegram.ext import Updater, CommandHandler
import os

# Получаем токен из переменной окружения
token = os.getenv('TELEGRAM_TOKEN')

def start(update, context):
    update.message.reply_text("Привет, я твой бот!")

def main():
    updater = Updater(token, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Используем метод polling, который не требует открытия порта
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



