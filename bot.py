import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Получаем токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_API_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот, запущенный на Railway 🚀")

def main():
    if not TOKEN:
        print("Ошибка: TELEGRAM_API_TOKEN не найден!")
        return

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    print("Бот запущен!")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
