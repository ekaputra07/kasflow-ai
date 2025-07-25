# kasflow
AI-powered personal expense tracker Telegram bot. Record expenses, view reports, and get insights.

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