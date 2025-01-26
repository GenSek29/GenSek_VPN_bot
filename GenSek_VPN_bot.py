from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler

# Счетчик
counter = 0

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> None:
    # Создание кнопки
    keyboard = [
        [InlineKeyboardButton("Увеличить счетчик", callback_data='increase')],
    ]
    
    # Создание разметки с кнопкой
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение с кнопкой
    await update.message.reply_text(f'Счетчик: {counter}', reply_markup=reply_markup)

# Обработчик нажатия кнопки
async def button(update: Update, context: CallbackContext) -> None:
    global counter
    query = update.callback_query
    await query.answer()
    
    # Если кнопка была нажата, увеличиваем счетчик
    if query.data == 'increase':
        counter += 1
    
    # Обновляем сообщение с новым значением счетчика
    await query.edit_message_text(text=f'Счетчик: {counter}', reply_markup=query.message.reply_markup)

def main():
    # Токен бота, полученный от BotFather
    token = '7734456717:AAFeMyZlA_Nv4ZwHM6Qt3s7M9AhW_d1advE'  # Замените на свой токен

    # Создание экземпляра Application
    application = Application.builder().token(token).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button))  # Обработчик кнопок

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()


