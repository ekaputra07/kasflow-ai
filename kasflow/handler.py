from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
from telegram.ext import filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm Kasflow, your personal expense tracker.")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"You said: {update.message.text}")


handlers = [
    CommandHandler("start", start),
    MessageHandler(filters.TEXT, message),
]
