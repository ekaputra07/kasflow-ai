import logging
from telegram.ext import ApplicationBuilder
from kasflow.handlers import all
from kasflow.conf import settings

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))


def run():
    app = ApplicationBuilder().token(settings.bot_token).build()
    app.add_handlers(all)
    app.run_polling()
