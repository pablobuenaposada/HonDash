clean:
	@rm -rf venv

virtualenv: clean
	virtualenv -p python3 venv
	. venv/bin/activate; pip install -r requirements.txt

run:
	. venv/bin/activate; sudo python src/bench/test.py

rpi:
	. venv/bin/activate; crossbar start &
	sleep 5
	pkill python backend.py || true
	. venv/bin/activate; python src/backend/backend.py &
	chromium-browser --kiosk src/frontend/frontend.html	

dummy:
	. venv/bin/activate; crossbar start &
	sleep 5
	pkill python dummy_backend.py || true
	. venv/bin/activate; python src/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/frontend.html

test:
	pytest src/tests --cov=./
