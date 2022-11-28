VIRTUAL_ENV ?= venv
PYTHON=$(VIRTUAL_ENV)/bin/python
PIP=$(VIRTUAL_ENV)/bin/pip
PYTEST=$(VIRTUAL_ENV)/bin/pytest
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
COVERALLS=$(VIRTUAL_ENV)/bin/coveralls
BLACK=$(VIRTUAL_ENV)/bin/black
PRETTIER=node_modules/.bin/prettier
PYTHON_VERSION=3.9
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
DOCKER_IMAGE=hondash
SYSTEM_DEPENDENCIES_UBUNTU= \
    $(PYTHON_WITH_VERSION) \
    $(PYTHON_WITH_VERSION)-dev \
    $(PYTHON_WITH_VERSION)-venv \
    build-essential \
    libsnappy-dev \
    libusb-1.0-0 \
    lsb-release \
    node-gyp \
    npm \
    python3-pip
SYSTEM_DEPENDENCIES_RASPBIAN= \
    libatlas-base-dev \
    libsnappy-dev \
    npm \
    python3-pandas
SYSTEM_DEPENDENCIES_MACOS= \
    snappy \
    npm \
    libusb
OS=$(shell lsb_release -si 2>/dev/null || uname)

system_dependencies:
ifeq ($(OS), Ubuntu)
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES_UBUNTU)
else ifeq ($(OS), Debian)
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES_RASPBIAN)
else ifeq ($(OS), Darwin)
	brew install $(SYSTEM_DEPENDENCIES_MACOS)
endif

clean:
	rm -rf $(VIRTUAL_ENV)

npm:
	npm install

$(VIRTUAL_ENV): npm
	$(PYTHON_WITH_VERSION) -m venv $(VIRTUAL_ENV)
	$(PYTHON) -m pip install --upgrade pip setuptools wheel
	$(PYTHON) -m pip install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

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
	docker-compose down -v || true
	docker stop hondash_app_1 || true
	docker stop hondash_nginx_1 || true
	sudo pkill -f src/backend || true
	sudo pkill -f http.server || true

test: lint
	PYTHONPATH=src $(PYTEST) --cov src/ src/tests
	@if [ -n "$$COVERALLS_REPO_TOKEN" ] && [ -f $(COVERALLS) ]; then $(COVERALLS); fi \

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

coveralls: virtualenv
	$(COVERALLS)

docker/build:
	docker build --no-cache --tag=$(DOCKER_IMAGE) .

docker/pull:
	docker pull $(DOCKER_IMAGE)

docker/run:
	PY_FILE=src/backend/main.py docker-compose up -d app nginx
	@echo Access http://localhost:8080/frontend/ for dashboard
	@echo Access http://localhost:8080/frontend/setup/ for setup
	@echo Access http://localhost:8080/frontend/datalogs/ for datalogs

docker/demo:
	PY_FILE=src/backend/bench/dummy_backend.py docker-compose up -d --build -V --force-recreate app nginx
	@echo Access http://localhost:8080/frontend/ for dashboard
	@echo Access http://localhost:8080/frontend/setup/ for setup
	@echo Access http://localhost:8080/frontend/datalogs/ for datalogs

docker/stop:
	docker-compose down --volume

docker/run/test:
	docker run --env-file docker.env $(DOCKER_IMAGE) /bin/sh -c 'make test'

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
