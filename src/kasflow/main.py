import logging
import argparse
import asyncio
from typing import Literal
from telegram.ext import ApplicationBuilder
from alembic.config import Config
from alembic import command

from kasflow.handlers import all
from kasflow.conf import settings

logging.basicConfig(level=getattr(logging, settings.log_level.upper()))
logger = logging.getLogger(__name__)


def run_db_migrations(path: str):
    # run db migrations
    try:
        alembic_cfg = Config(path)
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully.")
    except Exception as e:
        logger.error(f"Error during database migrations: {e}")


async def run_memory_setup():
    try:
        async with settings.memory_saver_class.from_conn_string(settings.memory_url) as memory:
            await memory.setup()
        logger.info("Memory setup completed successfully.")
    except Exception as e:
        logger.error(f"Error during memory setup: {e}")


def run_bot(mode: Literal["polling", "webhook"]):
    app = ApplicationBuilder().token(settings.bot_token).build()
    app.add_handlers(all)

    if mode == "polling":
        app.run_polling()

    elif mode == "webhook":
        app.run_webhook(
            webhook_url=settings.bot_webhook_url,
            listen=settings.bot_webhook_host,
            port=settings.bot_webhook_port,
            secret_token=settings.bot_webhook_secret_token,
        )


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        type=str,
        default="polling",
        choices=["polling", "webhook", "migrate"],
        help="Run the bot in polling or webhook mode or run db migrations",
    )
    parser.add_argument(
        "--alembic",
        type=str,
        default="alembic.ini",
        help="Path to alembic.ini file",
    )
    args = parser.parse_args()

    if args.mode == "migrate":
        run_db_migrations(args.alembic)
        asyncio.run(run_memory_setup())
    else:
        run_bot(args.mode)
