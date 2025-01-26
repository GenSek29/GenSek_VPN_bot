import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, MessageHandler, filters

# Подключаемся к базе данных
conn = sqlite3.connect('vpn_payments.db')
cursor = conn.cursor()

# Проверяем, если столбец "last_payment_date" отсутствует, добавляем его
cursor.execute("PRAGMA table_info(users);")
columns = [column[1] for column in cursor.fetchall()]
if 'last_payment_date' not in columns:
    cursor.execute('ALTER TABLE users ADD COLUMN last_payment_date TEXT')
    conn.commit()

# Устанавливаем дату следующей оплаты по умолчанию (для новых пользователей)
DEFAULT_PAYMENT_DATE = "01.02.2025"

# Создаем таблицу (если еще не создана)
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    next_payment_date TEXT,
    payment_status TEXT,
    last_payment_date TEXT
)
''')
conn.commit()

# Функция для старта бота
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name

    # Проверяем, есть ли пользователь в базе
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    keyboard = [["Я оплатил"]]  # Кнопка "Я оплатил"
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    if user is None:
        # Если пользователя нет, добавляем его с начальной датой
        cursor.execute('''
            INSERT INTO users (user_id, username, next_payment_date, payment_status, last_payment_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, DEFAULT_PAYMENT_DATE, 'Не оплачено', None))
        conn.commit()
        await update.message.reply_text(f'Привет, {username}! Ты добавлен в базу данных. Нажми /pay, чтобы оплатить.', reply_markup=reply_markup)
    else:
        # Если пользователь уже есть в базе, предлагаем ему оплатить
        await update.message.reply_text(f'С возвращением, {username}! Нажми /pay, чтобы оплатить.', reply_markup=reply_markup)

# Функция для отправки способов оплаты
async def pay(update: Update, context: CallbackContext) -> None:
    keyboard = [["Я оплатил"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        "Оплата возможна по номеру +79615912217 на Т-Банк.",
        reply_markup=reply_markup
    )

# Функция для подтверждения оплаты
async def confirm_payment(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    today = update.message.date.strftime("%d.%m.%Y")  # Текущая дата в формате ДД.ММ.ГГГГ

    # Получаем текущую дату следующей оплаты и текущую дату последней оплаты
    cursor.execute('SELECT next_payment_date, last_payment_date FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        next_payment_date = user[0]  # Текущая дата следующей оплаты
        last_payment_date = user[1]  # Дата последней оплаты
        print(f"Оплата подтверждена! Last Payment: {last_payment_date}, Next Payment: {next_payment_date}, User ID: {user_id}")  # Отладочный вывод

        # Обновляем базу: сохраняем дату последней оплаты и рассчитываем следующую дату
        cursor.execute('''
            UPDATE users
            SET last_payment_date = ?, next_payment_date = DATE(next_payment_date, '+1 month'), payment_status = 'Оплачено'
            WHERE user_id = ?
        ''', (today, user_id))
        conn.commit()

        # Печатаем, что изменения произошли
        print(f"Данные обновлены: Последняя оплата: {today}, Следующая оплата: {next_payment_date}, User ID: {user_id}")  # Отладочный вывод

        await update.message.reply_text(f"Спасибо за оплату! Следующая оплата: {next_payment_date}.")
    else:
        await update.message.reply_text("Ты не зарегистрирован. Нажми /start.")

# Основная функция для запуска бота
def main():
    token = '7734456717:AAFeMyZlA_Nv4ZwHM6Qt3s7M9AhW_d1advE'

    # Создаем приложение
    application = Application.builder().token(token).build()

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))  # Начальная команда
    application.add_handler(CommandHandler("pay", pay))  # Команда оплаты
    application.add_handler(MessageHandler(filters.Regex("Я оплатил"), confirm_payment))  # Обработчик кнопки

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
