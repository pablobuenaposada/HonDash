clean:
	@rm -rf venv

virtualenv: clean
	virtualenv -p python3.5 venv
	. venv/bin/activate; pip install -r requirements.txt

run:
	. venv/bin/activate; sudo python src/bench/test.py

make front:
	. venv/bin/activate; crossbar start &
	sleep 10
	. venv/bin/activate; pkill python backend.py || true
	. venv/bin/activate; python src/backend/backend.py &
	open -a "Google Chrome" src/frontend/frontend.html

test: virtualenv
	. venv/bin/activate; which pytest
