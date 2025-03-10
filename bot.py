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

# Функция для обработки команды /list (просмотр списка записей)
async def list_records(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, building, apartment, full_name, birth_year, article, status FROM records")
    records = cursor.fetchall()
    
    response = "Список записей:\n"
    for record in records:
        response += f"ID: {record[0]}, Корпус: {record[1]}, Квартира: {record[2]}, ФИО: {record[3]}, Год рождения: {record[4]}, Статья: {record[5]}, Статус: {record[6]}\n"
    
    await update.message.reply_text(response)
    cursor.close()
    conn.close()

# Функция для обработки команды /add (добавление записи)
async def add_record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем данные из команды (например, /add корпус квартира ФИО год_рождения статья статус)
        args = context.args
        if len(args) < 6:
            await update.message.reply_text("Использование: /add <корпус> <квартира> <ФИО> <год рождения> <статья> <статус>")
            return
        
        building = args[0]
        apartment = args[1]
        full_name = " ".join(args[2:4])  # Например, если ФИО состоит из двух частей
        birth_year = int(args[4])  # Преобразуем год рождения в целое число
        article = args[5]
        status = args[6] if len(args) > 6 else ""  # Статус может быть опциональным
        
        # Добавляем запись в базу данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO records (building, apartment, full_name, birth_year, article, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (building, apartment, full_name, birth_year, article, status))
        conn.commit()
        
        await update.message.reply_text(f"Запись добавлена: {full_name} (Корпус: {building}, Квартира: {apartment}, Год рождения: {birth_year}, Статья: {article}, Статус: {status})")
        
        cursor.close()
        conn.close()
    except Exception as e:
        await update.message.reply_text(f"Ошибка при добавлении записи: {e}")

# Функция для обработки команды /edit (редактирование записи)
async def edit_record(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем данные из команды (например, /edit id новый_корпус новый_апартамент)
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("Использование: /edit <id> <новый корпус> <новая квартира> <новый год рождения> <новая статья> <новый статус>")
            return
        
        record_id = args[0]
        new_building = args[1]
        new_apartment = args[2]
        new_birth_year = int(args[3])
        new_article = args[4]
        new_status = args[5]
        
        # Редактируем запись в базе данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE records SET building = %s, apartment = %s, birth_year = %s, article = %s, status = %s
            WHERE id = %s
        """, (new_building, new_apartment, new_birth_year, new_article, new_status, record_id))
        conn.commit()
        
        await update.message.reply_text(f"Запись с ID {record_id} обновлена.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        await update.message.reply_text(f"Ошибка при редактировании записи: {e}")

# Функция для обработки команды /history (просмотр истории изменений по имени)
async def view_history(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Получаем ФИО из команды (например, /history Иван Иванов)
        args = context.args
        if len(args) < 1:
            await update.message.reply_text("Использование: /history <ФИО>")
            return
        
        full_name = " ".join(args)
        
        # Получаем историю изменений из базы данных
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.updated_at, h.changes FROM history h
            JOIN records r ON h.record_id = r.id WHERE r.full_name = %s ORDER BY h.updated_at DESC
        """, (full_name,))
        history = cursor.fetchall()
        
        if not history:
            await update.message.reply_text(f"История изменений для {full_name} не найдена.")
            return
        
        response = f"История изменений для {full_name}:\n"
        for entry in history:
            response += f"{entry[0]} - {entry[1]}\n"
        
        await update.message.reply_text(response)
        
        cursor.close()
        conn.close()
    except Exception as e:
        await update.message.reply_text(f"Ошибка при получении истории: {e}")

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
    application.add_handler(CommandHandler("list", list_records))
    application.add_handler(CommandHandler("add", add_record))
    application.add_handler(CommandHandler("edit", edit_record))
    application.add_handler(CommandHandler("history", view_history))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
