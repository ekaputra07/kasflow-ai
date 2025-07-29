deps:
	uv sync

test:
	uv run pytest

run:
	export DATA_DIR=$(PWD)/data && uv run kasflow
