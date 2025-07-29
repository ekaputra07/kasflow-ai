# Kasflow 🤖
AI-powered Telegram bot for personal expense tracking, reporting and insights.

**Why I built this?**

Recently I'm learning [Langgraph](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/) for AI application development and my favorite way to learn is to build **real project** that I'll use myself. Develop an expense tracking bot on Telegram platform seems like good and viable idea.

```
- For personal use only, might not suitable for large records (backed by SQLite database).
- Currently no managed hosting solution so you have to host and run yourself.
- Feel free to fork and extend to suite your need. Contributions to this project are always welcomed.
```

**Features:**
- Record your expenses in natural language.
- Multi-turn conversation.
- Can be added to Group (for group expense tracking).
- Each user and group expense records are stored in separate database.
- Telegram command to list all expenses.

<a href="https://youtube.com/shorts/w70JmlZWY9g?feature=share" target="_blank">![](https://github.com/ekaputra07/kasflow-ai/blob/main/demo.gif)</a>

**Limitations:**
- Tested only on conversation in English and Indonesian. Let me know it it works with your language too.
- Tested only on `GPT-4.1-*` models, may or may not work on other models.
- Limited Telegram commands (more added soon).
- For simplicity it uses SQLite, might not scale well.
- Uses very basic RAG system, might not perform well on large expense records.

**Tech stack:**
- [Python Telegram Bot](https://python-telegram-bot.org/)
- [LangGraph](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/) (LLM workflows orchestration)
- OpenAI API (LLM provider)
- SQLite (expense records storage)

## Setup

Make sure you have [UV](https://docs.astral.sh/uv/) installed.

1. Install dependencies:
```bash
make deps
```

2. Create a `.env` file:
```bash
cp .env.example .env
```

3. Run the bot:
```bash
make run
```
