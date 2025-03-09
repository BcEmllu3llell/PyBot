import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Получение токена из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я простой Telegram-бот.')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Я могу помочь тебе! Используй /start для начала.')

def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def main() -> None:
    # Создание updater и dispatcher
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Обработчик сообщений (echo)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
