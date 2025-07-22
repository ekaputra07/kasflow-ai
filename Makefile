deps:
	uv lock && uv sync

run:
	uv run kasflow/main.py