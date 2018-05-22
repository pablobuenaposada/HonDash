from time import sleep
from autobahn_sync import publish, run

from devices.kpro import Kpro
from devices.time import Time
from devices.odometer import Odometer
from devices.formula import Formula

while True:
    try:
        run()
        break
    except:
        continue

kpro = Kpro()
time = Time()
odo = Odometer()

while True:
    odo.save(kpro.vss()['kmh'])
    publish('com.app.idea', {'bat': kpro.bat(),
                             'gear': kpro.gear(),
                             'iat': kpro.iat(),
                             'tps': kpro.tps(),
                             'ect': kpro.ect(),
                             'rpm': kpro.rpm(),
                             'vss': kpro.vss(),
                             'o2': kpro.o2(),
                             'cam': kpro.cam(),
                             'mil': kpro.mil(),
                             'bksw': kpro.bksw(),
                             'flr': kpro.flr(),
                             'map': kpro.map(),
                             'an0': Formula.psi_to_bar(Formula.ebay_150_psi(kpro.analog_input(0))),
                             'an1': Formula.autometer_2246(kpro.analog_input(1)),
                             'an2': Formula.vdo_323_057(kpro.analog_input(2)),
                             'an3': Formula.civic_eg_fuel_tank(kpro.analog_input(3)),
                             'an4': kpro.analog_input(4),
                             'an5': kpro.analog_input(5),
                             'an6': kpro.analog_input(6),
                             'an7': kpro.analog_input(7),
                             'time': time.get_time(),
                             'odo': odo.get_mileage(),
                             })
    sleep(0.1)
