import os
from random import randint
import logging
import vk_api as vk

from google.cloud import dialogflow
from vk_api.longpoll import VkLongPoll, VkEventType
from logs_handler import LogsHandler

logger = logging.getLogger('telegram_logger')


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text


def answer(event, vk_api):
    project_id = os.environ['GCP_PROJECT_ID']
    session_id = "vk-id" + str(event.user_id)
    dialogflow_response = detect_intent_texts(
        project_id, session_id, event.text, "ru")
    if dialogflow_response:
        vk_api.messages.send(
            user_id=event.user_id,
            message=dialogflow_response,
            random_id=randint(1, 1000)
        )


def main():
    vk_token = os.environ['VK_TOKEN']
    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    monitoring_telegram_token = os.environ['TELEGRAM_TOKEN_MONITORING']
    monitoring_chat_id = os.environ['CHAT_ID_MONITORING']

    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler(
        monitoring_telegram_token, monitoring_chat_id))
    logger.info("VkSupportBot запущен")

    try:
        longpoll = VkLongPoll(vk_session)
    except Exception:
        logger.exception()

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                answer(event, vk_api)
            except Exception:
                logger.exception()


if __name__ == "__main__":
    main()
