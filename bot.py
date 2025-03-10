import os
import psycopg2
from telegram import Update
from telegram.ext import CommandHandler, Application

# Получение переменной DATABASE_URL из окружения
DATABASE_URL = os.getenv('DATABASE_URL')

# Разбираем строку подключения
from urllib.parse import urlparse

parsed_url = urlparse(DATABASE_URL)

DB_HOST = parsed_url.hostname
DB_PORT = parsed_url.port
DB_USER = parsed_url.username
DB_PASSWORD = parsed_url.password
DB_NAME = parsed_url.path[1:]  # убираем начальный слэш

# Функция для подключения к базе данных
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Команда /add для добавления записи
async def add_record(update: Update, context):
    full_name = " ".join(context.args[:-1])  # Имя до последнего аргумента
    year = context.args[-1]  # Год — последний аргумент

    # Проверяем правильность ввода года
    try:
        year = int(year)
    except ValueError:
        await update.message.reply_text("Год должен быть числом.")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO records (full_name, year) VALUES (%s, %s)", (full_name, year))
        conn.commit()
        await update.message.reply_text(f"Запись '{full_name}' за {year} добавлена!")
    except psycopg2.Error as err:
        await update.message.reply_text(f"Ошибка при добавлении записи: {err}")
    finally:
        cursor.close()
        conn.close()

# Основная функция для запуска бота
async def main():
    # Токен вашего бота
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    # Создаем объект Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Команда /add
    application.add_handler(CommandHandler('add', add_record))

    # Запуск бота
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
