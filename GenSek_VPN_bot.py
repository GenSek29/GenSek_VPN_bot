from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Получаем токен из переменной окружения
token = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет, я твой бот!")

def main():
    # Используем Application вместо Updater
    application = Application.builder().token(token).build()

    # Регистрируем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Запускаем polling
    application.run_polling()

if __name__ == '__main__':
    main()




