IMAGE_NAME=ekaputra07/kasflow

deps:
	uv sync

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
	uv run kasflow --mode polling

migrate:
	uv run kasflow --mode=migrate --alembic alembic.ini

# usage: make docker.release v=1.0.0
docker.release:
	# build and release kasflow[sqlite] image
	echo "Building $(IMAGE_NAME):latest-sqlite and $(IMAGE_NAME):$(v)-sqlite"
	docker build -t $(IMAGE_NAME):latest-sqlite \
				 -t $(IMAGE_NAME):$(v)-sqlite \
				 --build-arg DB_ENGINE=sqlite \
				 .

	echo "Pushing $(IMAGE_NAME):latest-sqlite and $(IMAGE_NAME):$(v)-sqlite"
	docker push $(IMAGE_NAME):latest-sqlite
	docker push $(IMAGE_NAME):$(v)-sqlite

	# build and release kasflow[postgres] image
	echo "Building $(IMAGE_NAME):latest-postgres and $(IMAGE_NAME):$(v)-postgres"
	docker build -t $(IMAGE_NAME):latest-postgres \
				 -t $(IMAGE_NAME):$(v)-postgres \
				 --build-arg DB_ENGINE=postgres \
				 .

	echo "Pushing $(IMAGE_NAME):latest-postgres and $(IMAGE_NAME):$(v)-postgres"
	docker push $(IMAGE_NAME):latest-postgres
	docker push $(IMAGE_NAME):$(v)-postgres
