deps:
	uv sync --extra sqlite

test:
	uv run pytest

check:
	uv run ruff check

format:
	uv run ruff format

fix:
	uv run ruff check --fix


# check whether new migrations are needed
db.migrations.check:
	uv run alembic check

# usage: make db.migrations.generate name="create expenses table"
db.migrations.generate:
	uv run alembic revision --autogenerate -m "$(name)"

db.migrations.up:
	uv run alembic upgrade head

db.migrations.down:
	uv run alembic downgrade -1

run:
	uv run kasflow