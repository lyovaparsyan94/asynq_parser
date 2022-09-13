import asyncio
from threading import Thread

from core.handler import BaseHandler
from handlers.worker import Worker
from notifiers.telegram import bot


class Manager(BaseHandler):

    def __init__(self, config):
        self.urls = config['general']['urls']
        self.period = config['general']['period']
        self.notifiers_config = config['notifiers']
        self.telebot_polling_thread = Thread(target=bot.infinity_polling)
        self.telebot_polling_thread.start()

    async def start(self):
        workers = await self.initialize_workers()
        await self.run_workers(workers=workers)

    async def initialize_workers(self):
        workers = []
        for url in self.urls:
            worker = Worker(url=url, period=self.period, notifiers_config=self.notifiers_config)
            workers.append(worker)
        return workers

    @staticmethod
    async def run_workers(workers):
        for worker in workers:
            await asyncio.create_task(worker.start())
