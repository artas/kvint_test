import asyncio

import aiohttp
from bot.states import StateManager
from bot.base import BaseBot

memory_store = {}


class TelegramBot(BaseBot):
    def __init__(self, api_url, api_token, message_handler):
        super().__init__()
        self.api_url = api_url + api_token
        self.offset = -1
        self.memory_store = memory_store
        self.message_handler = message_handler

    async def send_message(self, user_id: int, text: str):
        async with aiohttp.ClientSession() as session:
            url = self.api_url + f'/sendMessage?chat_id={user_id}&text={text}'
            await session.post(url)

    async def get_updates(self):

        async with aiohttp.ClientSession() as session:
            url = self.api_url + f'/getUpdates?offset={self.offset}'
            response = await session.post(url)
            updates_json = await response.json()
        updates_result = updates_json.get('result')
        if updates_result:
            self.offset = updates_result[0].get('update_id') + 1
            for i in updates_result:
                chat_id = i['message'].get('from').get('id')
                if i['message']['text'] == '/start' or \
                        chat_id not in memory_store:
                    self.memory_store[chat_id] = StateManager(chat_id)
                    self.memory_store[chat_id].message = i['message']['text']

                    await self.message_handler(self, chat_id)
                else:
                    self.memory_store[chat_id].message = i['message']['text']
                    await self.message_handler(self, chat_id)
        asyncio.create_task(self.get_updates())
