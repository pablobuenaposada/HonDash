import random
from time import sleep

from autobahn_sync import publish, run

from devices.formula import Formula
from devices.odometer import Odometer
from devices.time import Time

run()

time = Time()
odo = Odometer()
while True:
    odo.save(random.randint(0, 200))
    publish(
        "com.app.idea",
        {
            "bat": random.uniform(0, 15),
            "map": {
                "bar": random.uniform(0, 2),
                "mbar": random.uniform(0, 2),
                "psi": random.uniform(0, 2),
            },
            "gear": random.randint(0, 6),
            "iat": {
                "celsius": random.randint(0, 50),
                "fahrenheit": random.randint(0, 50),
            },
            "tps": random.randint(0, 100),
            "ect": {
                "celsius": random.randint(0, 50),
                "fahrenheit": random.randint(0, 50),
            },
            "rpm": random.randint(0, 9000),
            "vss": {"kmh": random.randint(0, 200), "mph": random.randint(0, 200)},
            "o2": {"afr": random.uniform(0, 20), "lambda": random.uniform(0, 1)},
            "cam": random.randint(0, 50),
            "mil": random.choice([True, False]),
            "bksw": random.choice([True, False]),
            "an0": Formula.psi_to_bar(Formula.ebay_150_psi(random.uniform(0, 5))),
            "an1": Formula.autometer_2246(random.uniform(0, 5)),
            "an2": random.uniform(0, 5),
            "an3": random.uniform(0, 5),
            "an4": random.uniform(0, 5),
            "an5": random.uniform(0, 5),
            "an6": random.uniform(0, 5),
            "an7": random.uniform(0, 5),
            "di4": random.randint(0, 1),
            "di5": random.randint(0, 1),
            "di6": random.randint(0, 1),
            "di12": random.randint(0, 1),
            "di21": random.randint(0, 1),
            "di17": random.randint(0, 1),
            "di27": random.randint(0, 1),
            "di22": random.randint(0, 1),
            "time": time.get_time(),
            "odo": odo.get_mileage(),
            "ai0": Formula.vdo_323_057(random.uniform(0, 5)),
            "ai1": Formula.civic_eg_fuel_tank(random.uniform(0, 5)),
            "ai2": random.uniform(0, 5),
            "ai3": random.uniform(0, 5),
            "ai4": random.uniform(0, 5),
            "ai5": random.uniform(0, 5),
            "ai6": random.uniform(0, 5),
            "ai7": random.uniform(0, 5),
        },
    )
    sleep(0.1)
