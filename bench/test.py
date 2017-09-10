#sudo python bench/test.py
from __future__ import print_function
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.kpro import Kpro


kpro = Kpro()

while True:
    kpro.update()
    print("BAT: ", kpro.bat(), end='\r')
    print()
    print("CAM: ", kpro.cam(), end='\r')
    print()
    print("AFR: ", kpro.afr(), end='\r')
    print()
    print("IAT: ", kpro.iat(), end='\r')
    print()
    print("RPM: ", kpro.rpm(), end='\r')
    print()
    print("TPS: ", kpro.tps(), end='\r')
    print()
    print("VSS: ", kpro.vss(), end='\r')
    print()
