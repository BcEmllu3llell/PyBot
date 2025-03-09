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

# Запускаем бота в существующем цикле событий
if __name__ == "__main__":
    import asyncio

    # Если цикл событий уже запущен, не запускаем новый
    try:
        asyncio.get_event_loop().run_until_complete(main())  # Запускаем main() с текущим циклом событий
    except RuntimeError:
        asyncio.run(main())  # Если цикл событий еще не запущен, используем run()
