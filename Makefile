DOCKER_IMAGE=hondash-backend

venv:
	poetry install --without dev

venv-dev:
	poetry install

format: venv-dev
	poetry run black src
	poetry run ruff check src --fix

format/check: venv-dev
	poetry run black --verbose src --check
	poetry run ruff check src

test: venv-dev
	PYTHONPATH=src poetry run pytest src/tests

run: venv
	cp -n default_setup.json setup.json
	PYTHONPATH=src poetry run python src/main.py &

docker/build:
	docker build --no-cache --tag=$(DOCKER_IMAGE) .

docker/run:
	docker compose up --build -d

docker/tests:
	docker run --rm $(DOCKER_IMAGE) /bin/sh -c 'make test'
