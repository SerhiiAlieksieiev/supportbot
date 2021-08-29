import os
import dotenv
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from google.cloud import dialogflow
from logs_handler import LogsHandler

logger = logging.getLogger('telegram_logger')

def text_message(update, context):
    project_id = context.bot_data['project_id']

    text = update.message.text
    user_id = update.message.chat_id
    session_id = "tg-id" + str(user_id)
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        response = response.query_result.fulfillment_text
        
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=response)
    except Exception:
        logger.exception()


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def main():
    dotenv.load_dotenv('.env')
    telegram_token = os.environ['TELEGRAM_TOKEN']
    monitoring_telegram_token = os.environ['TELEGRAM_TOKEN_MONITORING']
    monitoring_chat_id = os.environ['CHAT_ID_MONITORING']
    
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(monitoring_telegram_token, monitoring_chat_id))
    logger.info("TelegramSupportBot запущен")

    try:
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

    except Exception:
        logger.exception()


if __name__ == '__main__':
    main()