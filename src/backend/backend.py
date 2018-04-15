from time import sleep
from autobahn_sync import publish, run
import sys
import os.path


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.kpro import Kpro
from devices.Time import Time
from devices.Odometer import Odometer
from devices.digital_input import DigitalInput
from devices.mcp3208 import Mcp3208

run()

kpro = Kpro()
time = Time()
odo = Odometer()
di4 = DigitalInput(4)
di17 = DigitalInput(17)
di27 = DigitalInput(27)
di22 = DigitalInput(22)
di21 = DigitalInput(21)
di6 = DigitalInput(6)
di5 = DigitalInput(5)
di12 = DigitalInput(12)
ai = Mcp3208()

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
                             'kan0': kpro.analog_input(0),
                             'time': time.get_time(),
                             'odo': odo.get_mileage(),
                             'di4': di4.status(),
                             'di17': di17.status(),
                             'di27': di27.status(),
                             'di22': di22.status(),
                             'di21': di21.status(),
                             'di6': di6.status(),
                             'di5': di5.status(),
                             'di12': di12.status(),
                             'ai0': ai.voltage(0),
                             'ai1': ai.voltage(1),
                             'ai2': ai.voltage(2),
                             'ai3': ai.voltage(3),
                             'ai4': ai.voltage(4),
                             'ai5': ai.voltage(5),
                             'ai6': ai.voltage(6),
                             'ai7': ai.voltage(7),
                             }
            )
    sleep(0.1)
