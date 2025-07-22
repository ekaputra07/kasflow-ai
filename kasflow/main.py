import os
from dotenv import load_dotenv

from kasflow.bots import poller_bot
from kasflow.handler import handlers

load_dotenv()


def run():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    poller_bot.run(token, handlers)
