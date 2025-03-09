import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Получаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_API_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Я бот на Railway 🚀")

async def main():
    if not TOKEN:
        print("Ошибка: TELEGRAM_API_TOKEN не найден!")
        return

    # Используем Application вместо Updater
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    print("Бот запущен!")
    # Запускаем бота
    await application.run_polling()

# Запуск без asyncio.run() для того, чтобы не нарушать уже существующий цикл событий
if __name__ == "__main__":
    import asyncio
    # Проверяем, если цикл событий уже существует, то используем его
    loop = asyncio.get_event_loop()
    loop.create_task(main())  # Запускаем задачу в текущем цикле
    loop.run_forever()  # Блокируем выполнение программы, пока бот работает
