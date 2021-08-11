import os
import dotenv
import logging

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow


def text_message(update, context):
    project_id = context.bot_data['project_id']

    text = update.message.text
    session_id = 123456789
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    response = response.query_result.fulfillment_text
    
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=response)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def main():
    dotenv.load_dotenv('.env')
    telegram_token = os.environ['TELEGRAM_TOKEN']
    
    updater = Updater(token=telegram_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['project_id'] = os.environ['GCP_PROJECT_ID']

    start_handeler = CommandHandler('start', start)
    text_message_handler = MessageHandler(Filters.text, text_message)

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    dispatcher.add_handler(start_handeler)
    dispatcher.add_handler(text_message_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()