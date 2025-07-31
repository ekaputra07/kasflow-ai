import logging
from telegram.ext import ApplicationBuilder
from kasflow.handlers import all
from kasflow.conf import settings

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))


def run():
    app = ApplicationBuilder().token(settings.bot_token).build()
    app.add_handlers(all)

    if settings.bot_mode == "polling":
        app.run_polling()

    elif settings.bot_mode == "webhook":
        app.run_webhook(
            webhook_url=settings.bot_webhook_url,
            listen=settings.bot_webhook_host,
            port=settings.bot_webhook_port,
            secret_token=settings.bot_webhook_secret_token,
        )
