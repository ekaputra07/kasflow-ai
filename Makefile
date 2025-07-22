deps:
	uv sync

test:
	uv run pytest

run:
	uv run kasflow