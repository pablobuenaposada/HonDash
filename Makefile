clean:
	@rm -rf venv

virtualenv: clean
	virtualenv -p python3 venv
	. venv/bin/activate; pip install -r requirements.txt

run:
	. venv/bin/activate; sudo python src/bench/test.py

rpi:
	. venv/bin/activate; crossbar start &
	pkill python backend.py || true
	-. venv/bin/activate; PYTHONPATH=/home/pi/Desktop/HonDash/src python src/backend/backend.py > /home/pi/Desktop/HonDash/hondash.log 2>&1 &
	chromium-browser --no-sandbox --kiosk --incognito src/frontend/frontend.html &

pc:
	. venv/bin/activate; crossbar start &
	pkill python backend.py || true
	. venv/bin/activate; PYTHONPATH=src python src/backend/backend.py &
	open -a "Google Chrome" src/frontend/frontend.html &

dummy:
	. venv/bin/activate; crossbar start &
	sleep 5
	pkill python dummy_backend.py || true
	. venv/bin/activate; python src/bench/dummy_backend.py &
	open -a "Google Chrome" src/frontend/frontend.html

test:
	pytest src/tests --cov=./
