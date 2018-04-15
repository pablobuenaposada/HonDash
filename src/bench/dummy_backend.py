import random
from time import sleep
from autobahn_sync import publish, call, register, subscribe, run
import sys
import os.path


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.Time import Time
from devices.odometer import Odometer

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
                             })
    sleep(0.1)
