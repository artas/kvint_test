import asyncio
from abc import ABC, abstractmethod


class BaseBot(ABC):

    @abstractmethod
    async def send_message(cls, user_id: int, text: str):
        pass

    @abstractmethod
    async def get_updates(cls):
        pass

    def run(self):
        while True:
            loop = asyncio.get_event_loop()
            loop.create_task(self.get_updates())
            try:
                loop.run_forever()
            except:
                pass
