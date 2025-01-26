from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Функция для старта бота
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Привет! Я бот, и я буду отвечать на твои сообщения.')

# Функция для ответа на любое сообщение (отправит обратно то же сообщение)
async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)

def main():
    # Указываем свой токен
    token = '7734456717:AAFeMyZlA_Nv4ZwHM6Qt3s7M9AhW_d1advE'

    # Создаем приложение с токеном
    application = Application.builder().token(token).build()

    # Команды
    application.add_handler(CommandHandler("start", start))

    # Обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Начинаем бота (он сам запускает цикл событий)
    application.run_polling()

if __name__ == '__main__':
    main()
