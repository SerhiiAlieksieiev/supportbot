import os
from random import randint
import dialogflow

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
            session=session, query_input=query_input)
    if response.query_result.intent.is_fallback:
        return None
    else:
        return response.query_result.fulfillment_text

def answer(event, vk_api):
    dotenv.load_dotenv('.env')
    project_id = os.environ['GCP_PROJECT_ID']
    dialogflow_response = detect_intent_texts(project_id, event.user_id, event.text, "ru")
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
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            answer(event, vk_api)
  

if __name__ == "__main__":
    main()