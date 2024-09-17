# PYTHONPATH=src python src/backend/bench/ecu.py
from __future__ import print_function

from backend.devices.ecu import Ecu
from reprint import output

ecu = Ecu()
with output(output_type="dict", initial_len=1, interval=0) as output_list:
    while True:
        output_list["ETH"] = str(ecu.eth)
        output_list["FLT"] = str(ecu.flt)
        output_list["BAT"] = str(ecu.bat)
        output_list["CAM"] = str(ecu.cam)
        output_list["O2"] = str(ecu.o2)
        output_list["O2_CMD"] = str(ecu.o2_cmd)
        output_list["IAT"] = str(ecu.iat)
        output_list["RPM"] = str(ecu.rpm)
        output_list["TPS"] = str(ecu.tps)
        output_list["VSS"] = str(ecu.vss)
        output_list["ECT"] = str(ecu.ect)
        output_list["GEAR"] = str(ecu.gear)
        output_list["EPS"] = str(ecu.eps)
        output_list["SCS"] = str(ecu.scs)
        output_list["RVSLCK"] = str(ecu.rvslck)
        output_list["BKSW"] = str(ecu.bksw)
        output_list["ACSW"] = str(ecu.acsw)
        output_list["ACCL"] = str(ecu.accl)
        output_list["FLR"] = str(ecu.flr)
        output_list["FANC"] = str(ecu.fanc)
        output_list["MAP"] = str(ecu.map)
        output_list["AN0"] = str(ecu.analog_input(0))
        output_list["AN1"] = str(ecu.analog_input(1))
        output_list["AN2"] = str(ecu.analog_input(2))
        output_list["AN3"] = str(ecu.analog_input(3))
        output_list["AN4"] = str(ecu.analog_input(4))
        output_list["AN5"] = str(ecu.analog_input(5))
        output_list["AN6"] = str(ecu.analog_input(6))
        output_list["AN7"] = str(ecu.analog_input(7))
        output_list["MIL"] = str(ecu.mil)
        output_list["ECU_TYPE"] = str(ecu.ecu_type)
        output_list["IGN"] = str(ecu.ign)
        output_list["SERIAL"] = str(ecu.serial)
        output_list["FIRMWARE"] = str(ecu.firmware)
