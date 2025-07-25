import logging
from kasflow.bots import poller_bot
from kasflow.handlers import all
from kasflow.conf import settings

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))


def run():
    poller_bot.run(settings.bot_token, all)
