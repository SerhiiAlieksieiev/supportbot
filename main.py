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
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    start_handeler = CommandHandler('start', start)
    dispatcher.add_handler(start_handeler)
    updater.start_polling()

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)


if __name__ == '__main__':
    main()
