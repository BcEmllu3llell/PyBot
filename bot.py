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

    # Используем Application для создания экземпляра бота
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    print("Бот запущен!")

    # Запускаем бота с использованием уже существующего цикла событий
    await application.run_polling()

# Обертка для вызова асинхронной функции main()
def start_bot():
    import asyncio
    asyncio.run(main())  # Запуск main() в синхронном контексте

# Запуск программы
if __name__ == "__main__":
    start_bot()
