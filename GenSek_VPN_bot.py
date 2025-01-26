from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
import os

app = Flask(__name__)

# Получаем токен из переменной окружения
token = os.getenv('TELEGRAM_TOKEN')

# Создаем объект приложения
application = Application.builder().token(token).build()

# Обработчик команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет, я твой бот! Напиши /help, чтобы узнать доступные команды.")

# Обработчик команды /help
async def help_command(update: Update, context):
    help_text = (
        "/start - Приветствие\n"
        "/help - Показать список команд\n"
        "/info - Информация о боте\n"
        "/echo <текст> - Повторить ваш текст"
    )
    await update.message.reply_text(help_text)

# Обработчик команды /info
async def info(update: Update, context):
    info_text = "Этот бот был создан для демонстрации базового функционала. Версия: 1.0"
    await update.message.reply_text(info_text)

# Обработчик команды /echo
async def echo(update: Update, context):
    # Получаем текст сообщения после команды /echo
    text = ' '.join(context.args)
    if text:
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("Ты не написал текст для повторения. Попробуй /echo <текст>.")

# Регистрируем обработчики команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(CommandHandler("info", info))
application.add_handler(CommandHandler("echo", echo))

@app.route('/webhook', methods=['POST'])
def webhook():
    # Получаем обновления от Telegram
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, application.bot)
    application.process_update(update)
    return "OK"

if __name__ == '__main__':
    # Устанавливаем webhook асинхронно
    async def set_webhook():
        webhook_url = os.getenv('WEBHOOK_URL')  # Например, URL твоего приложения на Render
        await application.bot.set_webhook(url=webhook_url + '/webhook')

    import asyncio
    asyncio.run(set_webhook())

    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
