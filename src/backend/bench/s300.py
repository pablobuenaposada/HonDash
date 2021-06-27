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
        output_list["SCS"] = str(s300.scs)
        output_list["MIL"] = str(s300.mil)
        output_list["ECT"] = str(s300.ect)
        output_list["FANC"] = str(s300.fanc)
        output_list["AN0"] = str(s300.analog_input(0))
        output_list["AN1"] = str(s300.analog_input(1))
        output_list["AN2"] = str(s300.analog_input(2))
        output_list["AN3"] = str(s300.analog_input(3))
        output_list["AN4"] = str(s300.analog_input(4))
        output_list["AN5"] = str(s300.analog_input(5))
        output_list["AN6"] = str(s300.analog_input(6))
        output_list["AN7"] = str(s300.analog_input(7))
