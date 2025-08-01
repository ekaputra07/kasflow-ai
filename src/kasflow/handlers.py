import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler
from telegram.ext import filters
from langchain_core.messages import HumanMessage

from kasflow.conf import settings
from kasflow.utils import format_currency, is_authorized
from kasflow.db.repository import ExpenseRepository
from kasflow.db.session import sessionmaker
from kasflow.graphs.main import MainGraph, MainState

logger = logging.getLogger(__name__)


UNAUTHORIZED_MESSAGE = "You are not authorized to use this bot."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message

    if not is_authorized(update):
        await message.reply_text(UNAUTHORIZED_MESSAGE)
        return

    greeting = settings.bot_greeting.format(bot_name=settings.bot_name)
    await message.reply_text(greeting)


async def list_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    List all expenses from user/group in the current chat.
    - On private user-bot chats, it lists user expenses.
    - On group chats, it lists group expenses.
    """
    message = update.message

    if not is_authorized(update):
        await message.reply_text(UNAUTHORIZED_MESSAGE)
        return

    thread_id = message.chat.id

    async with sessionmaker() as session:
        repo = ExpenseRepository(session)
        expenses = await repo.list_by_thread_id(thread_id)
        if expenses:
            formatted_expenses = "\n".join([e.as_list_item() for e in expenses])
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

    if not is_authorized(update):
        await message.reply_text(UNAUTHORIZED_MESSAGE)
        return

    thread_id = message.chat.id
    user_id = message.from_user.id

    async with settings.memory_saver_class.from_conn_string(settings.memory_url) as checkpointer:
        graph = MainGraph(checkpointer=checkpointer).compiled

        input = MainState(
            thread_id=thread_id,
            user_id=user_id,
            messages=[HumanMessage(content=message.text.lstrip("/"))],
        )

        output = await graph.ainvoke(
            input,
            {"configurable": {"thread_id": thread_id}},
        )

        if output.get("record_stored"):
            formatted_expenses = "\n".join(
                [
                    f"✓ {format_currency(e['amount'])} - {e['description']}"
                    for e in output["record_expenses"]
                ]
            )
            await update.message.reply_text(formatted_expenses)
        elif output.get("record_exception"):
            await update.message.reply_text(
                f"I couldn't store your expense record: {output['record_exception']}"
            )
        elif output.get("chat_response"):
            await update.message.reply_text(output["chat_response"])


all = [
    CommandHandler(
        command="start",
        callback=start,
        filters=~filters.UpdateType.EDITED_MESSAGE,
    ),
    CommandHandler(
        command="list",
        callback=list_expenses,
        filters=~filters.UpdateType.EDITED_MESSAGE,
    ),
    MessageHandler(
        filters=(filters.TEXT & ~filters.UpdateType.EDITED_MESSAGE),
        callback=message,
    ),
]
