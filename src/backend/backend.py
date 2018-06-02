from time import sleep
from autobahn_sync import publish, run

from devices.kpro import Kpro
from devices.time import Time
from devices.odometer import Odometer

from mapper import Mapper


while True:
    try:
        run()
        break
    except:
        continue

map = Mapper()
kpro = Kpro()
time = Time()
odo = Odometer()
while True:
    odo.save(kpro.vss()['kmh'])
    publish('com.app.idea', {'bat': kpro.bat(),
                             'gear': kpro.gear(),
                             'iat': kpro.iat().setdefault(map.get_unit('iat'), 'celsius'),
                             'tps': kpro.tps(),
                             'ect': kpro.ect().setdefault(map.get_unit('ect'), 'celsius'),
                             'rpm': kpro.rpm(),
                             'vss': kpro.vss().setdefault(map.get_unit('vss'), 'kmh'),
                             'o2': kpro.o2().setdefault(map.get_unit('o2'), 'afr'),
                             'cam': kpro.cam(),
                             'mil': kpro.mil(),
                             'bksw': kpro.bksw(),
                             'flr': kpro.flr(),
                             'map': kpro.map().setdefault(map.get_unit('map'), 'bar'),
                             'an0': map.get_formula('an0')(kpro.analog_input(0)).setdefault(map.get_unit('an0'), 'volts'),
                             'an1': map.get_formula('an1')(kpro.analog_input(1)).setdefault(map.get_unit('an1'), 'volts'),
                             'an2': map.get_formula('an2')(kpro.analog_input(2)).setdefault(map.get_unit('an2'), 'volts'),
                             'an3': map.get_formula('an3')(kpro.analog_input(3)).setdefault(map.get_unit('an3'), 'volts'),
                             'an4': map.get_formula('an4')(kpro.analog_input(4)).setdefault(map.get_unit('an4'), 'volts'),
                             'an5': map.get_formula('an5')(kpro.analog_input(5)).setdefault(map.get_unit('an5'), 'volts'),
                             'an6': map.get_formula('an6')(kpro.analog_input(6)).setdefault(map.get_unit('an6'), 'volts'),
                             'an7': map.get_formula('an7')(kpro.analog_input(7)).setdefault(map.get_unit('an7'), 'volts'),
                             'time': time.get_time(),
                             'odo': odo.get_mileage(),
                             })
    sleep(0.1)

