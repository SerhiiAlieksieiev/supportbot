import os
import dotenv
import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def main():
    dotenv.load_dotenv('.env')
    telegram_token = os.environ['TELEGRAM_TOKEN']
    # Проверка бота
    # print(bot.get_me())
    # Настройки
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    # Хендлеры
    start_handeler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_handeler)
    dispatcher.add_handler(echo_handler)

    # Начинаем поиск обновлений
    updater.start_polling()

    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()
