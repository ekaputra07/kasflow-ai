from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
from telegram.ext import filters

from kasflow.conf import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greeting = settings.greeting_message.format(bot_name=settings.bot_name)
    await update.message.reply_text(greeting)


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"You said: {update.message.text}")


handlers = [
    CommandHandler("start", start),
    MessageHandler(filters.TEXT, message),
]
