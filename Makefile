VIRTUAL_ENV ?= venv
PYTHON=$(VIRTUAL_ENV)/bin/python
PIP=$(VIRTUAL_ENV)/bin/pip
PYTEST=$(VIRTUAL_ENV)/bin/pytest
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
COVERALLS=$(VIRTUAL_ENV)/bin/coveralls
BLACK=$(VIRTUAL_ENV)/bin/black
CROSSBAR=$(VIRTUAL_ENV)/bin/crossbar
PYTHON_VERSION=3.7
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
DOCKER_IMAGE=pablobuenaposada/hondash
SYSTEM_DEPENDENCIES_UBUNTU=$(PYTHON_WITH_VERSION) $(PYTHON_WITH_VERSION)-dev \
	virtualenv lsb-release pkg-config git build-essential libssl-dev tox \
	libsnappy-dev python3-pip
SYSTEM_DEPENDENCIES_RASPBIAN=virtualenv libatlas-base-dev libsnappy-dev
OS=$(shell lsb_release -si 2>/dev/null || uname)

system_dependencies:
ifeq ($(OS), Ubuntu)
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES_UBUNTU)
else ifeq ($(OS), Raspbian)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES_RASPBIAN)
endif

clean:
	py3clean .
	rm -rf $(VIRTUAL_ENV)

$(VIRTUAL_ENV):
	virtualenv --python=$(PYTHON_WITH_VERSION) $(VIRTUAL_ENV)
	$(PIP) install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

run: virtualenv
	cp -n default_setup.json setup.json
	$(CROSSBAR) start &
	pkill python backend.py || true
	PYTHONPATH=src $(PYTHON) src/backend/backend.py &
	open -a "Google Chrome" src/frontend/index.html &

run_rpi:
	cp -n default_setup.json setup.json
	$(CROSSBAR) start &
	sudo PYTHONPATH=src $(PYTHON) src/backend/backend.py &
	sleep 5
	chromium-browser --kiosk --incognito src/frontend/index.html &

dummy:
	$(CROSSBAR) start &
	sleep 5
	pkill python dummy_backend.py || true
	$(PYTHON) src/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/index.html

test: lint
	PYTHONPATH=src $(PYTEST) --cov src/ src/tests
	@if [ -n "$$CI" ] && [ -f $(COVERALLS) ]; then $(COVERALLS); fi \

lint/isort-fix: virtualenv
	$(ISORT) -rc src

lint/isort-check: virtualenv
	$(ISORT) -rc -c src

lint/flake8: virtualenv
	$(FLAKE8) src

lint/black-fix: virtualenv
	$(BLACK) --exclude $(VIRTUAL_ENV) src

lint/black-check: virtualenv
	$(BLACK) --exclude $(VIRTUAL_ENV) src --check

lint: lint/isort-check lint/flake8 lint/black-check

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
	wget -c https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
	chmod +x pishrink.sh
	sudo ./pishrink.sh full_size_image.img shrinked_image.img
