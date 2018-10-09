# sudo python bench/test.py
from __future__ import print_function

from reprint import output

from devices.kpro import Kpro

kpro = Kpro()
with output(output_type="dict", initial_len=1, interval=0) as output_list:
    while True:
        output_list['ETH'] = str(kpro.eth())
        output_list['FLT'] = str(kpro.flt())
        output_list['BAT'] = str(kpro.bat())
        output_list['CAM'] = str(kpro.cam())
        output_list['O2'] = str(kpro.o2())
        output_list['IAT'] = str(kpro.iat())
        output_list['RPM'] = str(kpro.rpm())
        output_list['TPS'] = str(kpro.tps())
        output_list['VSS'] = str(kpro.vss())
        output_list['ECT'] = str(kpro.ect())
        output_list['GEAR'] = str(kpro.gear())
        output_list['EPS'] = str(kpro.eps())
        output_list['SCS'] = str(kpro.scs())
        output_list['RVSLCK'] = str(kpro.rvslck())
        output_list['BKSW'] = str(kpro.bksw())
        output_list['ACSW'] = str(kpro.acsw())
        output_list['ACCL'] = str(kpro.accl())
        output_list['FLR'] = str(kpro.flr())
        output_list['FANC'] = str(kpro.fanc())
        output_list['MAP'] = str(kpro.map())
        output_list['AN0'] = str(kpro.analog_input(0))
        output_list['AN1'] = str(kpro.analog_input(1))
        output_list['AN2'] = str(kpro.analog_input(2))
        output_list['AN3'] = str(kpro.analog_input(3))
        output_list['AN4'] = str(kpro.analog_input(4))
        output_list['AN5'] = str(kpro.analog_input(5))
        output_list['AN6'] = str(kpro.analog_input(6))
        output_list['AN7'] = str(kpro.analog_input(7))
        output_list['MIL'] = str(kpro.mil())
        output_list['ECU_TYPE'] = str(kpro.ecu_type())
        output_list['IGN'] = str(kpro.ign())
        output_list['SERIAL'] = str(kpro.serial())
        output_list['FIRMWARE'] = str(kpro.firmware())
