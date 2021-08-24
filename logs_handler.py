import logging
import telegram

class LogsHandler(logging.Handler):

    def __init__(self, token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.token = token

    def emit(self, record):
        log_entry = self.format(record)
        tg_bot = telegram.Bot(self.token)
        tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
