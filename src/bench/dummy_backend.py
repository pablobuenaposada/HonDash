import random
from time import sleep
from autobahn_sync import publish, call, register, subscribe, run
from src.devices.time import Time
from src.devices.odometer import Odometer

run()

time = Time()
odo = Odometer()
while True:
    odo.save(random.randint(0, 200))
    publish('com.app.idea', {'bat': random.uniform(0, 15),
                             'gear': random.randint(0, 6),
                             'iat': random.randint(0, 50),
                             'tps': random.randint(0, 100),
                             'ect': random.randint(0, 150),
                             'rpm': random.randint(0, 9000),
                             'vss': random.randint(0, 200),
                             'afr': random.uniform(0, 2),
                             'cam': random.randint(0, 50),
                             'an0': random.uniform(0, 5),
                             'time': time.get_time(),
                             'odo': odo.get_mileage(),
                             'left_turn_signal': random.randint(0, 1),
                             'right_turn_signal': random.randint(0, 1),
                             'reserve': random.randint(0, 1),
                             'battery': random.randint(0, 1),
                             'mil': random.randint(0, 1),
                             'handbrake': random.randint(0, 1),
                             'high_beam': random.randint(0, 1),
                             'trunk': random.randint(0, 1),
                             'oil_warning': random.randint(0, 1),
                             })
    sleep(0.1)
