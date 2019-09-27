VIRTUAL_ENV ?= venv
PYTHON=$(VIRTUAL_ENV)/bin/python
PIP=$(VIRTUAL_ENV)/bin/pip
PYTEST=$(VIRTUAL_ENV)/bin/pytest
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
CROSSBAR=$(VIRTUAL_ENV)/bin/crossbar
PYTHON_VERSION=3
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
SYSTEM_DEPENDENCIES=$(PYTHON_WITH_VERSION) $(PYTHON_WITH_VERSION)-dev \
	virtualenv lsb-release pkg-config git build-essential libssl-dev tox \
	libsnappy-dev
OS=$(shell lsb_release -si 2>/dev/null || uname)

system_dependencies:
ifeq ($(OS), Ubuntu)
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

clean:
	py3clean .
	rm -rf $(VIRTUAL_ENV)

$(VIRTUAL_ENV):
	virtualenv -p $(PYTHON_WITH_VERSION) $(VIRTUAL_ENV)
	$(PIP) install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

virtualenv_rpi:
	pip install virtualenv
	sudo /usr/bin/easy_install virtualenv==16.0.0
	virtualenv -p $(PYTHON_WITH_VERSION) $(VIRTUAL_ENV)
	$(PIP) install -r requirements.txt

run: virtualenv
	$(CROSSBAR) start &
	pkill python backend.py || true
	PYTHONPATH=src $(PYTHON) src/backend/backend.py &
	open -a "Google Chrome" src/frontend/index.html &

run_rpi:
	$(CROSSBAR) start &
	pkill python backend.py || true
	sudo -E PYTHONPATH=src $(PYTHON) src/backend/backend.py &
	sleep 5
	chromium-browser --kiosk --incognito src/frontend/index.html &

dummy:
	$(CROSSBAR) start &
	sleep 5
	pkill python dummy_backend.py || true
	$(PYTHON) src/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/index.html

test: lint
	PYTHONPATH=src $(PYTEST) src/tests --cov=./

lint/isort-fix: virtualenv
	$(ISORT) -rc src

lint/isort-check: virtualenv
	$(ISORT) -rc -c src

lint/flake8: virtualenv
	$(FLAKE8) src

lint: lint/isort-check lint/flake8

docker/build:
	docker build --tag=hondash .

docker/run/test:
	docker run hondash /bin/sh -c 'make test'

docker/run/shell:
	docker run -it --rm hondash
