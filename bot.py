import os
import psycopg2
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен и URL базы данных из окружения
TOKEN = os.getenv('TELEGRAM_API_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

# Функция для подключения к базе данных
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я Telegram бот, и я готов работать!')

# Функция для обработки команды /add (добавление записи)
async def add_record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем данные из команды (например, /add ФИО 2025)
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("Использование: /add <ФИО> <год>")
            return
        
        full_name = " ".join(args[:-1])  # Имя до последнего аргумента
        year = args[-1]  # Год — последний аргумент

        # Проверяем правильность ввода года
        try:
            year = int(year)
        except ValueError:
            await update.message.reply_text("Год должен быть числом.")
            return
        
        # Добавляем запись в базу данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO records (full_name, year) VALUES (%s, %s)", (full_name, year))
        conn.commit()
        
        await update.message.reply_text(f"Запись добавлена: {full_name} ({year})")
        
        cursor.close()
        conn.close()
    except Exception as e:
        await update.message.reply_text(f"Ошибка при добавлении записи: {e}")

# Основная функция для запуска бота
def main():
    # Проверяем наличие токена
    if not TOKEN:
        print("Ошибка: TELEGRAM_API_TOKEN не найден в окружении.")
        return

    # Создаем объект Application для взаимодействия с API
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_record))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
