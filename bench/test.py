#sudo python bench/test.py
from __future__ import print_function
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.kpro import Kpro
from reprint import output


kpro = Kpro()
with output(output_type="dict", initial_len=1, interval=0) as output_list:
    while True:
        output_list['BAT'] = str(kpro.bat())
        output_list['CAM'] = str(kpro.cam())
        output_list['AFR'] = str(kpro.afr())
        output_list['IAT'] = str(kpro.iat())
        output_list['RPM'] = str(kpro.rpm())
        output_list['TPS'] = str(kpro.tps())
        output_list['VSS'] = str(kpro.vss())
        output_list['ECT'] = str(kpro.ect())
