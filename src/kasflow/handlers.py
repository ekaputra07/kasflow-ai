import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
from telegram.ext import filters
from langchain_core.messages import HumanMessage
from kasflow.conf import settings
from kasflow.utils import database_path, format_currency, is_group_update
from kasflow.store import init_store
from kasflow.graphs.main import MainGraph, MainState

logger = logging.getLogger(__name__)

# initialize graphs
graph = MainGraph().compiled


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    greeting = settings.bot_greeting.format(bot_name=settings.bot_name)
    await update.message.reply_text(greeting)


async def list_expenses(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    List all expenses from user/group in the current chat.
    - On private user-bot chats, it lists user expenses.
    - On group chats, it lists group expenses.
    """
    message = update.message
    thread_id = message.chat.id
    db_ext = ".group.db" if is_group_update(update) else ".user.db"
    db_path = database_path(thread_id, ext=db_ext)

    async with init_store(db_path) as store:
        expenses = await store.list_expenses()
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
    """
    Create expense(s) for user/group in the current chat.
    - On private user-bot chats, it creates user expenses.
    - On group chats, it creates group expenses but each expense
      is assigned to the user who sent the message.

    Group and user expenses are stored in separate databases.
    """

    message = update.message
    if not message:
        return

    thread_id = message.chat.id
    user_id = message.from_user.id
    db_ext = ".group.db" if is_group_update(update) else ".user.db"
    db_path = database_path(thread_id, ext=db_ext)

    async with init_store(db_path) as store:
        input = MainState(
            db_path=db_path,
            messages=[HumanMessage(content=message.text)],
        )
        output = await graph.ainvoke(
            input,
            {
                "configurable": {
                    "store": store,
                    "thread_id": thread_id,
                    "user_id": user_id,
                }
            },
        )

        if output.get("record_stored"):
            formatted_expenses = "\n".join(
                [
                    f"✓ {format_currency(e.amount)} - {e.description}"
                    for e in output["record_expenses"]
                ]
            )
            await update.message.reply_text(formatted_expenses)
        elif output.get("record_exception"):
            await update.message.reply_text(
                f"I couldn't store your expense record: {output['store_exception']}"
            )
        elif output.get("chat_response"):
            await update.message.reply_text(output["chat_response"])


all = [
    CommandHandler("start", start),
    CommandHandler("list", list_expenses),
    MessageHandler(filters.TEXT, message),
]
