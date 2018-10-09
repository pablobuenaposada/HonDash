ISORT="venv/bin/isort"
FLAKE8="venv/bin/flake8"

clean:
	@rm -rf venv

virtualenv: clean
	virtualenv -p python3 venv
	. venv/bin/activate; pip install -r requirements.txt

virtualenv_rpi: clean
	pip install virtualenv
	sudo /usr/bin/easy_install virtualenv
	virtualenv -p python3 venv
	. venv/bin/activate; pip install -r requirements.txt

run:
	. venv/bin/activate; crossbar start &
	pkill python backend.py || true
	. venv/bin/activate; PYTHONPATH=src python src/backend/backend.py &
	open -a "Google Chrome" src/frontend/index.html &

run_rpi:
	. venv/bin/activate; crossbar start &
	pkill python backend.py || true
	sudo -E PYTHONPATH=src ./venv/bin/python src/backend/backend.py &
	sleep 5
	chromium-browser --kiosk --incognito src/frontend/index.html &

dummy:
	. venv/bin/activate; crossbar start &
	sleep 5
	pkill python dummy_backend.py || true
	. venv/bin/activate; python src/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/index.html

test: isort lint
	pytest src/tests --cov=./

isort:
	$(ISORT) -rc src

lint:
	$(FLAKE8) src
