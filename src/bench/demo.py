import random
from time import sleep

from devices.kpro import constants
from devices.kpro.kpro import Kpro
from main import Backend

backend = Backend()
backend.ecu.ecu = Kpro()
backend.ecu.ecu.status = True
backend.ecu.ecu.version = 4
backend.ecu.ecu.data0 = [0 for _ in range(38)]
backend.ecu.ecu.data1 = [0 for _ in range(7)]
backend.ecu.ecu.data3 = [0 for _ in range(100)]
backend.ecu.ecu.data4 = [0 for _ in range(18)]
backend.ecu.ecu.data5 = [0 for _ in range(20)]

while True:
    numbers = range(255)
    numbers = numbers if bool(random.getrandbits(1)) else reversed(numbers)
    for number in numbers:
        backend.ecu.ecu.data0 = [number for _ in range(38)]
        backend.ecu.ecu.data1 = [number for _ in range(7)]
        backend.ecu.ecu.data3 = [number for _ in range(100)]
        backend.ecu.ecu.data4 = [number for _ in range(18)]
        backend.ecu.ecu.data5 = [number for _ in range(20)]
        backend.ecu.ecu.data0[constants.KPRO4_GEAR] = random.choice(range(1, 7))
        backend.ecu.ecu.data3[constants.KPRO4_AN0_1] = 121
        backend.ecu.ecu.data3[constants.KPRO4_AN0_2] = 121
        # backend.logger.active = bool(random.getrandbits(1))
        sleep(0.1)
