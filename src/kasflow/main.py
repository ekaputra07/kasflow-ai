from kasflow.bots import poller_bot
from kasflow.handler import handlers
from kasflow.conf import settings


def run():
    poller_bot.run(settings.bot_token, handlers)
