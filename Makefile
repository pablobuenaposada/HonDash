DOCKER_IMAGE=hondash-backend

venv:
	poetry install --without dev

venv-dev:
	poetry install

format: venv-dev
	poetry run black src
	poetry run ruff check src --fix
	npx dclint . -r --fix

format/check: venv-dev
	poetry run black --verbose src --check
	poetry run ruff check src

test: venv-dev
	PYTHONPATH=src poetry run pytest src/tests

run_rpi:
	sudo cp -n default_setup.json setup.json
	sudo PYTHONPATH=src poetry run python /home/pi/Desktop/HonDash/src/main.py

docker/build:
	docker build --no-cache --tag=$(DOCKER_IMAGE) .

docker/run:
	docker compose up --build -d

docker/demo:
	docker compose up --build -d nginx
	docker compose run -p 5678:5678 --build -d app poetry run python src/bench/demo.py

docker/tests:
	docker run --rm $(DOCKER_IMAGE) /bin/sh -c 'make test'

sd-image/create: # use diskutil list first, usage make sd-image/create path=/dev/rdisk6
	sudo dd bs=1024 if=$(path) of=full_size_image.img

sd-image/shrink:
	docker run --privileged=true --rm --volume $(shell pwd):/workdir monsieurborges/pishrink pishrink -v full_size_image.img shrinked_image.img
