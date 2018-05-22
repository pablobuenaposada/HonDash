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
	open -a "Google Chrome" src/frontend/frontend.html &

run_rpi:
	. venv/bin/activate; crossbar start &
	pkill python backend.py || true
	sudo -E PYTHONPATH=src ./venv/bin/python src/backend/backend.py &
	chromium-browser --kiosk --incognito src/frontend/frontend.html &

dummy:
	. venv/bin/activate; crossbar start &
	sleep 5
	pkill python dummy_backend.py || true
	. venv/bin/activate; python src/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/frontend.html

test:
	pytest src/tests --cov=./
