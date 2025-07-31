deps:
	uv sync --extra sqlite

test:
	uv run pytest

# usage: make db.migrations.generate name="create expenses table"
db.migrations.generate:
	uv run alembic revision --autogenerate -m "$(name)"

db.migrations.up:
	uv run alembic upgrade head

db.migrations.down:
	uv run alembic downgrade -1

run:
	export DATA_DIR=$(PWD)/data && uv run kasflow
