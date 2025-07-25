# kasflow
AI-powered Telegram bot for personal expense tracking, reporting and insights.

Tech stack:
- Python Telegram Bot
- LangGraph (LLM workflows orchestration)
- OpenAI API (LLM provider)
- SQLite (expense records storage)

## Setup

Install dependencies:
```bash
make deps
```

Create a `.env` file:
```bash
cp .env.example .env
```


## Run

Run the bot:
```bash
make run
```