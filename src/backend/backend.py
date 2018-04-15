from time import sleep
from autobahn_sync import publish, run
import sys
import os.path


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.kpro import Kpro
from devices.Time import Time
from devices.Odometer import Odometer

run()

kpro = Kpro()
time = Time()
odo = Odometer()

while True:
    odo.save(kpro.vss())
    publish('com.app.idea', {'bat': kpro.bat(),
                             'gear': kpro.gear(),
                             'iat': kpro.iat(),
                             'tps': kpro.tps(),
                             'ect': kpro.ect(),
                             'rpm': kpro.rpm(),
                             'vss': kpro.vss(),
                             'afr': kpro.afr(),
                             'cam': kpro.cam(),
                             'an0': kpro.analog_input(0),
                             'time': time.get_time(),
                             'odo': odo.get_mileage(),
                             'di22':
                             })
    sleep(0.1)
