import os
from dotenv import load_dotenv

from bots import poller_bot
from handler import handlers

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    poller_bot.run(token, handlers)
