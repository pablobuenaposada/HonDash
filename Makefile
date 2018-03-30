PIP=`. venv/bin/activate; which pip`
PYTHON=`. venv/bin/activate; which python`
DEPS:=requirements/requirements.txt
PYTEST=`. venv/bin/activate; which pytest`
PYTHON_VERSION=python3.5

clean:
	@rm -rf venv

virtualenv: clean
	virtualenv -p $(PYTHON_VERSION) venv
	. venv/bin/activate; pip install -r $(DEPS)

run:
	. venv/bin/activate; sudo python bench/test.py

make front:
	. venv/bin/activate; crossbar start &
	sleep 10
	. venv/bin/activate; pkill python backend.py || true
	. venv/bin/activate; python backend/backend.py &
	open -a "Google Chrome" frontend/frontend.html

test: virtualenv
	$(PYTEST)
