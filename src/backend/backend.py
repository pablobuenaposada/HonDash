from time import sleep
from autobahn_sync import publish, run

from devices.kpro import Kpro
from devices.time import Time
from devices.odometer import Odometer
from devices.digital_input import DigitalInput
from devices.analog_inputs import AnalogInputs
from devices.formula import Formula

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
ai = AnalogInputs()

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
                             'mil': kpro.mil(),
                             'bksw': kpro.bksw(),
                             'map': kpro.map(),
                             'an0': Formula.psi_to_bar(Formula.ebay_150_psi(kpro.analog_input(0))),
                             'an1': Formula.autometer_2246(kpro.analog_input(1)),
                             'an2': kpro.analog_input(2),
                             'an3': kpro.analog_input(3),
                             'an4': kpro.analog_input(4),
                             'an5': kpro.analog_input(5),
                             'an6': kpro.analog_input(6),
                             'an7': kpro.analog_input(7),
                             'di4': di4.status(),
                             'di5': di5.status(),
                             'di6': di6.status(),
                             'di12': di12.status(),
                             'di17': di17.status(),
                             'di21': di21.status(),
                             'di22': di22.status(),
                             'di27': di27.status(),
                             'time': time.get_time(),
                             'odo': odo.get_mileage(),
                             'ai0': Formula.vdo_323_057(ai.voltage(0)),
                             'ai1': Formula.civic_eg_fuel_tank(ai.voltage(1)),
                             'ai2': ai.voltage(2),
                             'ai3': ai.voltage(3),
                             'ai4': ai.voltage(4),
                             'ai5': ai.voltage(5),
                             'ai6': ai.voltage(6),
                             'ai7': ai.voltage(7),
                             })
    sleep(0.1)
