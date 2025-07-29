# Kasflow 🤖
Kasflow (or _Cashflow_) is an AI-powered Telegram bot for personal expense tracking, reporting and insights.

```
Disclaimer:
- For personal use only, might not suitable for large records (backed by SQLite database).
- Currently no managed hosting solution so you have to host and run yourself.
- Feel free to fork and extend to suite your need. Contributions to this project are always welcomed.
```

**👉 Features:**
- Record your expenses in natural language (tested on English and Indonesian).
- Multi-turn conversations.
- Can be added to Group (for group expense tracking).
- Each user and group expense records are stored in separate database.
- Telegram command to list all expenses.

<a href="https://youtube.com/shorts/w70JmlZWY9g?feature=share" target="_blank">![](https://github.com/ekaputra07/kasflow-ai/blob/main/demo.gif)</a>

**👉 Why built this?**

Recently I stumbled upon [Langgraph](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/) for AI application development. Keen to try it out myself and to build a **real project** that I'll actually use is the most fun way to learn. Develop an expense tracking bot on Telegram platform seems like good and viable idea.

**👉 Limitations:**
- Tested only on conversation in English and Indonesian. Let me know it it works with your language too.
- Tested only on `GPT-4.1-*` models, may or may not work on other models and providers.
- Limited Telegram commands (more added soon).
- For simplicity it uses SQLite, might not scale well.
- Uses very basic RAG system, might not perform well on large expense records.

**👉 Tech stack:**
- [Python Telegram Bot](https://python-telegram-bot.org/)
- [LangGraph](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/) (LLM workflows orchestration)
- OpenAI API (LLM provider)
- SQLite (expense records storage)

## Setup

### Option 1: Local Development

Make sure you have [UV](https://docs.astral.sh/uv/) installed.

1. Install dependencies:
```bash
make deps
```

2. Create a `.env` file:
```bash
# Required environment variables:
BOT_TOKEN=your-telegram-token
OPENAI_API_KEY=your-openai-api-key
BOT_NAME=Kasflow
```

3. Run the bot:
```bash
make run
```

### Option 2: Docker

1. Create a `.env` file with your configuration:
```bash
# Required environment variables:
BOT_TOKEN=your-telegram-token
OPENAI_API_KEY=your_openai_api_key_here
BOT_NAME=Kasflow
```

2. Build and run with Docker Compose:
```bash
docker-compose up
```