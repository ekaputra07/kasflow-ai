import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
from telegram.ext import filters

from kasflow.conf import settings
from kasflow.utils import db_path, format_currency
from kasflow.store.duckdb import DuckDBStore
from kasflow.graphs.recorder import RecorderGraph, RecorderState

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greeting = settings.greeting_message.format(bot_name=settings.bot_name)
    await update.message.reply_text(greeting)


async def list_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user:
        with DuckDBStore(db_path(update.effective_user.id)) as store:
            expenses = store.list_expense()
            formatted_expenses = "\n".join(
                [f"{e.created.strftime('%b %d %H:%M')} - {format_currency(e.amount)} - {e.description}" for e in expenses]
            )
            await update.message.reply_text(f"{formatted_expenses}")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user:
        with DuckDBStore(db_path(update.effective_user.id)) as store:
            compiled = RecorderGraph().compiled
            in_state = RecorderState(message=update.message.text)
            out_state = compiled.invoke(in_state, {"configurable": {"store": store}})
            if out_state.get("stored"):
                formatted_expenses = "\n".join(
                    [f"✓ {format_currency(e.amount)} - {e.description}" for e in out_state["expenses"]]
                )
                await update.message.reply_text(formatted_expenses)
            elif out_state.get("store_exception"):
                await update.message.reply_text(f"I couldn't store your expense record: {out_state['store_exception']}")
            else:
                await update.message.reply_text("I don't know what to do with your message.")


all = [
    CommandHandler("start", start),
    CommandHandler("list", list_expenses),
    MessageHandler(filters.TEXT, message),
]
