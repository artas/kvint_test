import os
from bot import TelegramBot
from scenario import message_handler

if __name__ == '__main__':
    scenario = message_handler
    bot_url = os.getenv('API_URL')
    api_token = os.getenv('API_TOKEN')
    bot = TelegramBot(bot_url, api_token, scenario)
    bot.run()