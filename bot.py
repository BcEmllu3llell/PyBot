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
        # Получаем данные из команды (например, /add корпус квартира ФИО год_рождения статус)
        args = context.args
        if len(args) < 4:
            await update.message.reply_text("Использование: /add <корпус> <квартира> <ФИО> <год рождения> <статус>")
            return
        
        building = args[0]
        apartment = args[1]
        full_name = " ".join(args[2:-2])  # Собираем все слова как ФИО
        birth_year = int(args[-2])  # Год рождения
        status = args[-1]  # Статус
        
        # Добавляем запись в базу данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO records (building, apartment, full_name, birth_year, status) VALUES (%s, %s, %s, %s, %s)",
                       (building, apartment, full_name, birth_year, status))
        conn.commit()
        
        await update.message.reply_text(f"Запись добавлена: {full_name} (Корпус: {building}, Квартира: {apartment}, Год рождения: {birth_year}, Статус: {status})")
        
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
