import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
from telegram.ext import filters
from kasflow.conf import settings
from kasflow.utils import db_path, format_currency
from kasflow.store.aiosqlite import AioSQLiteStore
from kasflow.graphs.recorder import RecorderGraph, RecorderState

logger = logging.getLogger(__name__)

# initialize graphs
recorder = RecorderGraph().compile()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greeting = settings.greeting_message.format(bot_name=settings.bot_name)
    await update.message.reply_text(greeting)


async def list_expenses(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user = update.effective_user
    if user:
        async with AioSQLiteStore(db_path(user.id)) as store:
            expenses = await store.list_expense()
            if expenses:
                formatted_expenses = "\n".join(
                    [
                        f"{e.created.strftime('%b %d %H:%M')} - {format_currency(e.amount)} - {e.description}"
                        for e in expenses
                    ]
                )
                await update.message.reply_text(f"{formatted_expenses}")
            else:
                await update.message.reply_text("No expenses found.")


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user:
        thread_id = user.id
        async with AioSQLiteStore(db_path(thread_id)) as store:
            input = RecorderState(message=update.message.text)
            output = await recorder.ainvoke(
                input,
                {"configurable": {"store": store, "thread_id": thread_id}},
            )

            if output.get("stored"):
                formatted_expenses = "\n".join(
                    [
                        f"✓ {format_currency(e.amount)} - {e.description}"
                        for e in output["expenses"]
                    ]
                )
                await update.message.reply_text(formatted_expenses)
            elif output.get("store_exception"):
                await update.message.reply_text(
                    f"I couldn't store your expense record: {output['store_exception']}"
                )
            else:
                await update.message.reply_text(
                    "I don't know what to do with your message."
                )


all = [
    CommandHandler("start", start),
    CommandHandler("list", list_expenses),
    MessageHandler(filters.TEXT, message),
]
