from time import sleep

from autobahn_sync import publish, register, run

from devices.kpro import Kpro
from devices.odometer import Odometer
from devices.setup_file import SetupFile
from devices.time import Time


@register(u'setup')
def setup():
    return setup.load_setup()


@register(u'save')
def save(new_setup):
    setup.save_setup(new_setup)


while True:
    try:
        run()
        break
    except:
        continue

kpro = Kpro()
time = Time()
odo = Odometer()
setup = SetupFile()

iat_unit = setup.json.get('iat', {}).get('unit', 'celsius')
ect_unit = setup.json.get('ect', {}).get('unit', 'celsius')
vss_unit = setup.json.get('vss', {}).get('unit', 'kmh')
o2_unit = setup.json.get('o2', {}).get('unit', 'afr')
odo_unit = setup.json.get('odo', {}).get('unit', 'km')
map_unit = setup.json.get('map', {}).get('unit', 'bar')
an0_unit = setup.json.get('an0', {}).get('unit', 'volts')
an1_unit = setup.json.get('an1', {}).get('unit', 'volts')
an2_unit = setup.json.get('an2', {}).get('unit', 'volts')
an3_unit = setup.json.get('an3', {}).get('unit', 'volts')
an4_unit = setup.json.get('an4', {}).get('unit', 'volts')
an5_unit = setup.json.get('an5', {}).get('unit', 'volts')
an6_unit = setup.json.get('an6', {}).get('unit', 'volts')
an7_unit = setup.json.get('an7', {}).get('unit', 'volts')

an0_formula = setup.get_formula('an0')
an1_formula = setup.get_formula('an1')
an2_formula = setup.get_formula('an2')
an3_formula = setup.get_formula('an3')
an4_formula = setup.get_formula('an4')
an5_formula = setup.get_formula('an5')
an6_formula = setup.get_formula('an6')
an7_formula = setup.get_formula('an7')

while True:
    odo.save(kpro.vss()['kmh'])
    publish('data', {'bat': kpro.bat(),
                     'gear': kpro.gear(),
                     'iat': kpro.iat()[iat_unit],
                     'tps': kpro.tps(),
                     'ect': kpro.ect()[ect_unit],
                     'rpm': kpro.rpm(),
                     'vss': kpro.vss()[vss_unit],
                     'o2': kpro.o2()[o2_unit],
                     'cam': kpro.cam(),
                     'mil': kpro.mil(),
                     'fan': kpro.fanc(),
                     'bksw': kpro.bksw(),
                     'flr': kpro.flr(),
                     'eth': kpro.eth(),
                     'map': kpro.map()[map_unit],
                     'an0': an0_formula(kpro.analog_input(0))[an0_unit],
                     'an1': an1_formula(kpro.analog_input(1))[an1_unit],
                     'an2': an2_formula(kpro.analog_input(2))[an2_unit],
                     'an3': an3_formula(kpro.analog_input(3))[an3_unit],
                     'an4': an4_formula(kpro.analog_input(4))[an4_unit],
                     'an5': an5_formula(kpro.analog_input(5))[an5_unit],
                     'an6': an6_formula(kpro.analog_input(6))[an6_unit],
                     'an7': an7_formula(kpro.analog_input(7))[an7_unit],
                     'time': time.get_time(),
                     'odo': odo.get_mileage()[odo_unit],
                     })
    sleep(0.1)
