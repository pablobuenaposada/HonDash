DOCKER_IMAGE=hondash-backend

venv:
	uv sync --no-dev

venv-dev:
	uv sync

format: venv-dev
	uv run ruff format src
	uv run ruff check src --fix
	npx dclint . -r --fix

format/check: venv-dev
	uv run ruff format --check src
	uv run ruff check src

test: venv-dev
	PYTHONPATH=src uv run pytest src/tests

run_rpi:
	sudo cp -n default_setup.json setup.json
	sudo PYTHONPATH=src uv run --no-sync python /home/pi/Desktop/HonDash/src/main.py

docker/build:
	docker build --no-cache --tag=$(DOCKER_IMAGE) .

docker/run:
	docker compose up --build -d

docker/demo:
	docker compose up --build -d nginx
	docker compose run -p 5678:5678 --build -d app python src/bench/demo.py

docker/tests:
	docker run --rm $(DOCKER_IMAGE) /bin/sh -c 'make test'

sd-image/create: # use diskutil list first, usage make sd-image/create path=/dev/rdisk6
	sudo dd bs=1024 if=$(path) of=full_size_image.img

sd-image/shrink:
	docker run --privileged=true --rm --volume $(shell pwd):/workdir monsieurborges/pishrink pishrink -v full_size_image.img shrinked_image.img
