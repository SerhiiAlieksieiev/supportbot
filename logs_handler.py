import logging
import telegram

class LogsHandler(logging.Handler):

    def __init__(self, token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token)

    def emit(self, record):
        log_entry = self.format(record)
        tg_bot = self.bot
        tg_bot.send_message(chat_id=self.chat_id, text=log_entry)
