import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Получаем токен из окружения
TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я Telegram бот, и я готов работать!')

# Основная функция для запуска бота
def main():
    # Проверяем наличие токена
    if not TOKEN:
        print("Ошибка: TELEGRAM_API_TOKEN не найден в окружении.")
        return

    # Создаем updater и dispatcher
    updater = Updater(TOKEN)

    # Получаем dispatcher
    dispatcher = updater.dispatcher

    # Регистрируем обработчик команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Запуск бота
    updater.start_polling()

    # Бот работает до остановки
    updater.idle()

if __name__ == '__main__':
    main()
