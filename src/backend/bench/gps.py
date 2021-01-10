# PYTHONPATH=src python src/backend/bench/gps.py

from reprint import output

from backend.devices.gps import Gps

gps = Gps()
with output(output_type="dict", initial_len=1, interval=0) as output_list:
    while True:
        output_list["SPEED"] = str(gps.speed)
        output_list["STATUS"] = str(gps.status)
