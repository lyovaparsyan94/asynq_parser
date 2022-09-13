import asyncio
import aiohttp
from bs4 import BeautifulSoup

from core.handler import BaseHandler
from notifiers.telegram import TelegramNotifier


class Worker(BaseHandler):
    def __init__(self, url, period, notifiers_config):
        self.url = url
        self.base_url = "https://list.am"
        self.period = period
        self.__homes_info = {}
        self.__new_homes = {}
        self.telegram_notifier = TelegramNotifier(config=notifiers_config["telegram"], worker=self)
        self.initial_run = True

    async def start(self):
        try:
            while True:
                items = await self.parse()
                self.get_and_collect_info(items=items)
                if not self.initial_run:
                    self.send_new_homes_notification()
                    self._clear_new_homes_dic()
                else:
                    self.initial_run = False
                await asyncio.sleep(self.period)
        except Exception as e:
            print(f"Exception occurred: {e}")

    async def parse(self):
        html = await self.get_page_html()
        soup = BeautifulSoup(markup=html, features='html.parser')
        div = soup.findAll('div', {'class': 'dl'})
        items = self.get_sections(div=div)

        return items

    async def get_page_html(self):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(self.url, ssl=False) as response:
                html = await response.text()
        return html

    @staticmethod
    def get_sections(div):
        items = []
        for item in div:
            elements = item.findChildren("a", recursive=False)
            items.extend(elements)
        return items

    def get_and_collect_info(self, items):
        for item in items:
            link = f"{self.base_url}/{item['href']}"
            home_info = item.select('.dl a > div > div')
            title, price, description, *update = [element.text for element in home_info]
            update = self.set_update_value(update=update)
            place, rooms, area, flor = description.split(', ')
            self.collect_home_data(link=link, title=title, price=price, place=place, rooms=rooms, area=area, flor=flor,
                                   update=update)

    def collect_home_data(self, **kwargs):
        title = kwargs.get('title')
        if title not in self.__homes_info:
            self.__homes_info[title] = {}
            self.__new_homes[title] = {}
            self.__homes_info[title].update(kwargs)
            self.__new_homes[title].update(kwargs)

    def send_new_homes_notification(self):
        if self.__new_homes:
            self.telegram_notifier.send(homes=self.__new_homes)

    def _clear_new_homes_dic(self):
        self.__new_homes.clear()

    def get_all_homes(self):
        return self.__homes_info

    def get_new_homes(self):
        return self.__new_homes

    @staticmethod
    def set_update_value(update):
        if not update:
            return "---"
        return update[0]
