DOCKER_IMAGE=hondash-backend

venv:
	poetry install --without dev

venv-dev:
	poetry install

test: venv-dev
	PYTHONPATH=src poetry run pytest src/tests

docker/build:
	docker build --no-cache --tag=$(DOCKER_IMAGE) .

docker/run:
	docker-compose up --build -d

docker/run/test:
	docker run $(DOCKER_IMAGE) /bin/sh -c 'make test'
