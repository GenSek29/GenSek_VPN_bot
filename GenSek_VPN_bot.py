from telegram import Bot
from telegram.ext import Application, CommandHandler

async def start(update, context):
    await update.message.reply_text('Привет, я твой бот!')

async def main():
    token = '7734456717:AAFeMyZlA_Nv4ZwHM6Qt3s7M9AhW_d1advE'
    application = Application.builder().token(token).build()
    
    # Регистрируем хендлеры
    application.add_handler(CommandHandler('start', start))
    
    # Запускаем бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
