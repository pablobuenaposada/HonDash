DOCKER_IMAGE=hondash

venv:
	poetry install --without dev

venv-dev:
	poetry install

run: virtualenv
	cp -n default_setup.json setup.json || true
	$(PYTHON) -m http.server &
	PYTHONPATH=src $(PYTHON) src/backend/main.py &
	open http://localhost:8000/src/frontend/ &

run_rpi:
	cp -n default_setup.json setup.json
	sudo PYTHONPATH=src $(PYTHON) src/backend/main.py &
	sleep 5
	chromium-browser --use-gl=egl --kiosk --check-for-update-interval=604800 --incognito http://hondash.local/ &

dummy:
	cp -n default_setup.json setup.json || true
	PYTHONPATH=src $(PYTHON) src/backend/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/index.html

kill:
	docker compose down -v || true
	docker stop hondash_app_1 || true
	docker stop hondash_nginx_1 || true
	sudo pkill -f src/backend || true
	sudo pkill -f http.server || true

test: venv-dev
	PYTHONPATH=src poetry run pytest src/tests

lint/isort-fix: virtualenv
	$(ISORT) src

lint/isort-check: virtualenv
	$(ISORT) --diff -c src

lint/flake8: virtualenv
	$(FLAKE8) src

lint/black-fix: virtualenv
	$(BLACK) --exclude $(VIRTUAL_ENV) src

lint/black-check: virtualenv
	$(BLACK) --exclude $(VIRTUAL_ENV) src --check

lint/prettier-check: npm
	$(PRETTIER) --check "src/frontend/**"

lint/prettier-fix: npm
	$(PRETTIER) --write "src/frontend/**"

lint-fix: lint/isort-fix lint/black-fix lint/prettier-fix

lint: lint/isort-check lint/flake8 lint/black-check lint/prettier-check

docker/build:
	docker build --no-cache --tag=$(DOCKER_IMAGE) .

docker/pull:
	docker pull $(DOCKER_IMAGE)

docker/run:
	PY_FILE=src/backend/main.py docker compose up -d
	@echo Access http://localhost:8080/frontend/ for dashboard
	@echo Access http://localhost:8080/frontend/setup/ for setup
	@echo Access http://localhost:8080/frontend/datalogs/ for datalogs

docker/demo:
	PY_FILE=src/backend/bench/dummy_backend.py docker compose up -d --build -V --force-recreate app nginx
	@echo Access http://localhost:8080/frontend/ for dashboard
	@echo Access http://localhost:8080/frontend/setup/ for setup
	@echo Access http://localhost:8080/frontend/datalogs/ for datalogs

docker/stop:
	docker compose down --volume

docker/run/test:
	docker run $(DOCKER_IMAGE) /bin/sh -c 'make test'

docker/run/shell:
	docker run -it --rm $(DOCKER_IMAGE)

docker/run/lint:
	docker run $(DOCKER_IMAGE) /bin/sh -c 'make lint'

sd-image/create:
	sudo dd bs=1024 if=$(path) of=full_size_image.img

sd-image/shrink:
	docker run --privileged=true --rm --volume $(shell pwd):/workdir mgomesborges/pishrink pishrink -v full_size_image.img shrinked_image.img

demo: virtualenv
	cp -n default_setup.json setup.json || true
	$(PYTHON) -m http.server &
	PYTHONPATH=src $(PYTHON) src/backend/bench/dummy_backend.py &
	open http://localhost:8000/src/frontend/ &
