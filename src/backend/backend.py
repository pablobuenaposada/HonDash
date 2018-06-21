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

kpro = Kpro()
time = Time()
odo = Odometer()
map = Mapper()

iat_unit = map.get_unit('iat')
ect_unit = map.get_unit('ect')
vss_unit = map.get_unit('vss')
o2_unit = map.get_unit('o2')
map_unit = map.get_unit('map')
an0_unit = map.get_unit('an0')
an0_formula = map.get_formula('an0')
an1_unit = map.get_unit('an1')
an1_formula = map.get_formula('an1')
an2_unit = map.get_unit('an2')
an2_formula = map.get_formula('an2')
an3_unit = map.get_unit('an3')
an3_formula = map.get_formula('an3')
an4_unit = map.get_unit('an4')
an4_formula = map.get_formula('an4')
an5_unit = map.get_unit('an5')
an5_formula = map.get_formula('an5')
an6_unit = map.get_unit('an6')
an6_formula = map.get_formula('an6')
an7_unit = map.get_unit('an7')
an7_formula = map.get_formula('an7')

while True:
    odo.save(kpro.vss()['kmh'])
    publish('com.app.idea', {'bat': kpro.bat(),
                             'gear': kpro.gear(),
                             'iat': kpro.iat().setdefault(iat_unit, 'celsius'),
                             'tps': kpro.tps(),
                             'ect': kpro.ect().setdefault(ect_unit, 'celsius'),
                             'rpm': kpro.rpm(),
                             'vss': kpro.vss().setdefault(vss_unit, 'kmh'),
                             'o2': kpro.o2().setdefault(o2_unit, 'afr'),
                             'cam': kpro.cam(),
                             'mil': kpro.mil(),
                             'bksw': kpro.bksw(),
                             'flr': kpro.flr(),
                             'map': kpro.map().setdefault(map_unit, 'bar'),
                             'eth': kpro.eth(),
                             'an0': an0_formula(kpro.analog_input(0)).setdefault(an0_unit, 'volts'),
                             'an1': an1_formula(kpro.analog_input(1)).setdefault(an1_unit, 'volts'),
                             'an2': an2_formula(kpro.analog_input(2)).setdefault(an2_unit, 'volts'),
                             'an3': an3_formula(kpro.analog_input(3)).setdefault(an3_unit, 'volts'),
                             'an4': an4_formula(kpro.analog_input(4)).setdefault(an4_unit, 'volts'),
                             'an5': an5_formula(kpro.analog_input(5)).setdefault(an5_unit, 'volts'),
                             'an6': an6_formula(kpro.analog_input(6)).setdefault(an6_unit, 'volts'),
                             'an7': an7_formula(kpro.analog_input(7)).setdefault(an7_unit, 'volts'),
                             'time': time.get_time(),
                             'odo': odo.get_mileage(),
                             })
    sleep(0.1)

