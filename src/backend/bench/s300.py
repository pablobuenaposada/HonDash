# PYTHONPATH=src python src/backend/bench/s300.py
from __future__ import print_function

from reprint import output

from backend.devices.s300.s300 import S300

s300 = S300()
with output(output_type="dict", initial_len=1, interval=0) as output_list:
    while True:
        output_list["BAT"] = str(s300.bat)
        output_list["TPS"] = str(s300.tps)
        output_list["RPM"] = str(s300.rpm)
