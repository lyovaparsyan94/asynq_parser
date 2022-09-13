import telebot

from core.notifier import BaseNotifier
from config.mapping import RU_MAPPING

bot = telebot.TeleBot(token="YOUR TOKEN HERE")


class TelegramNotifier(BaseNotifier):
    instance = None

    def __init__(self, config, worker):
        self.updates_chat_id = config["chat_ids"]["new_homes_chat_id"]
        self.all_homes_chat_id = config["chat_ids"]["all_homes"]
        self.worker = worker
        TelegramNotifier.instance = self

    @staticmethod
    def create_message(homes):
        messages = []
        text = ''
        count = 1
        for name, home in homes.items():
            tmp_text = "".join(f"{RU_MAPPING[key]}: {value}\n" for key, value in home.items())
            text = f"{text}{tmp_text}{10 * '='}\n"
            if len(text) >= 3600 or count == len(text):
                messages.append(text)
                text = ''
            count += 1

        return messages

    def send(self, homes, homes_history=False):
        chat_id = self.all_homes_chat_id if homes_history else self.updates_chat_id
        messages = self.create_message(homes=homes)
        for message in messages:
            bot.send_message(chat_id=chat_id, text=message)

    @staticmethod
    @bot.message_handler(commands=['all'])
    def send_all_homes(message):
        self = TelegramNotifier.instance
        homes = self.worker.get_all_homes()
        self.send(homes=homes, homes_history=True)
