from time import sleep
from autobahn_sync import publish, call, register, subscribe, run
import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.kpro import Kpro

run()

kpro = Kpro()
while True:
    publish('com.app.idea', {'bat': kpro.bat(),
                             'iat': kpro.iat(),
                             'tps': kpro.tps(),
                             'ect': kpro.ect(),
                             'rpm': kpro.rpm(),
                             'vss': kpro.vss(),
                             'afr': kpro.afr(),
                             'cam': kpro.cam(),
                             'an0': kpro.an0()
                             })
    sleep(0.1)