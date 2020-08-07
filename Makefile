VIRTUAL_ENV ?= venv
PYTHON=$(VIRTUAL_ENV)/bin/python
PIP=$(VIRTUAL_ENV)/bin/pip
PYTEST=$(VIRTUAL_ENV)/bin/pytest
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
COVERALLS=$(VIRTUAL_ENV)/bin/coveralls
BLACK=$(VIRTUAL_ENV)/bin/black
PRETTIER=node_modules/.bin/prettier
PYTHON_VERSION=3.7
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
DOCKER_IMAGE=pablobuenaposada/hondash
SYSTEM_DEPENDENCIES_UBUNTU= \
    $(PYTHON_WITH_VERSION) \
    $(PYTHON_WITH_VERSION)-dev \
    build-essential \
    git \
    libsnappy-dev \
    libssl1.0-dev \
    lsb-release \
    node-gyp \
    nodejs-dev \
    npm \
    pkg-config \
    python3-pip \
    tox \
    virtualenv
SYSTEM_DEPENDENCIES_RASPBIAN= \
    libatlas-base-dev \
    libsnappy-dev \
    virtualenv \
    npm
SYSTEM_DEPENDENCIES_MACOS= \
    snappy \
    npm
OS=$(shell lsb_release -si 2>/dev/null || uname)

system_dependencies:
ifeq ($(OS), Ubuntu)
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES_UBUNTU)
else ifeq ($(OS), Raspbian)
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES_RASPBIAN)
else ifeq ($(OS), Darwin)
	brew install $(SYSTEM_DEPENDENCIES_MACOS)
endif

clean:
	py3clean .
	rm -rf $(VIRTUAL_ENV)

npm:
	npm install

$(VIRTUAL_ENV): npm
	virtualenv --python=$(PYTHON_WITH_VERSION) $(VIRTUAL_ENV)
	$(PIP) install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

run: virtualenv
	cp -n default_setup.json setup.json || true
	PYTHONPATH=src $(PYTHON) src/backend/main.py &
	open -a "Google Chrome" src/frontend/index.html &

run_rpi:
	cp -n default_setup.json setup.json
	sudo PYTHONPATH=src $(PYTHON) src/backend/main.py &
	sleep 5
	chromium-browser --kiosk --incognito src/frontend/index.html &

dummy:
	cp -n default_setup.json setup.json || true
	PYTHONPATH=src $(PYTHON) src/backend/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/index.html

kill:
	sudo pkill -f backend || true

test: lint
	PYTHONPATH=src $(PYTEST) --cov src/ src/tests
	@if [ -n "$$CI" ] && [ -f $(COVERALLS) ]; then $(COVERALLS); fi \

lint/isort-fix: virtualenv
	$(ISORT) -rc src

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
	docker build --cache-from=$(DOCKER_IMAGE):latest --tag=$(DOCKER_IMAGE) .

docker/pull:
	docker pull $(DOCKER_IMAGE)

docker/run/test:
	docker run --env-file docker.env $(DOCKER_IMAGE) /bin/sh -c 'make test'

docker/run/shell:
	docker run -it --rm $(DOCKER_IMAGE)

docker/run/lint:
	docker run $(DOCKER_IMAGE) /bin/sh -c 'make lint'

sd-image/create:
	sudo dd bs=1024 if=$(path) of=full_size_image.img

sd-image/shrink:
	git clone https://github.com/deepeeess/PiShrink.git
	chmod +x PiShrink/pishrink.sh
	mv full_size_image.img PiShrink/
	cd PiShrink; docker-compose run pishrink /pishrink/pishrink.sh /pishrink/full_size_image.img
