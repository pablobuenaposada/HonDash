# PYTHONPATH=src uv run python src/bench/demo.py
import random
from time import sleep

from devices.kpro import constants
from devices.kpro.kpro import Kpro
from main import Backend

TICK = 0.1  # seconds per update, everything below is tuned around this

# roughly a K20 with a six speed box on 205/50R16s
GEAR_RATIOS = (3.267, 2.130, 1.517, 1.147, 0.921, 0.738)
FINAL_DRIVE = 4.764
WHEEL_CIRCUMFERENCE = 1.95  # metres per wheel revolution
# how hard it pulls in each gear, m/s^2 at full throttle
GEAR_PULL = {1: 4.6, 2: 3.7, 3: 2.9, 4: 2.2, 5: 1.6, 6: 1.1}

IDLE_RPM = 950
IDLE_HUNT = 22  # rpm of wander per tick, an idle never sits perfectly still
IDLE_SETTLE = 0.06  # how hard it is pulled back towards IDLE_RPM
# each run up the road picks its own shift point and throttle, so no two
# launches look the same
SHIFT_UP_RPM = (7000, 8300)
SHIFT_DOWN_RPM = 3200
PEDAL = (70, 100)  # % throttle held while accelerating
CRUISE_RPM = 4000  # shifts up while cruising to settle around here
MAX_RPM = 8600
BRAKING = 8.0  # m/s^2
DRAG = 0.0003  # quadratic; low enough that it can still pull to the shift point
# how fast it gets before backing off, picked fresh for each run up the road
CRUISE_SPEED = (80, 180)  # km/h


def rpm_for(speed_kmh, gear):
    """Engine speed the gearing implies for a given road speed"""
    wheel_revs_per_sec = (speed_kmh / 3.6) / WHEEL_CIRCUMFERENCE
    return wheel_revs_per_sec * GEAR_RATIOS[gear - 1] * FINAL_DRIVE * 60


class Car:
    """
    Drives itself round in a loop: pulls away, runs up through the gearbox,
    cruises for a bit, brakes back down to a stop, waits, goes again.

    Speed, revs and gear stay consistent with each other because revs are
    always derived from road speed through the gearing, so the dashboard
    behaves the way a real one would.
    """

    def __init__(self):
        self.speed = 0.0  # km/h
        self.rpm = IDLE_RPM
        self.tps = 0.0  # %
        self.gear = 0  # 0 is neutral
        self.state = "idle"
        self.countdown = 1.0
        self._new_run()

    def _new_run(self):
        """Fresh target, shift point and throttle for the next run up the road"""
        self.target = random.uniform(*CRUISE_SPEED)
        self.shift_rpm = random.uniform(*SHIFT_UP_RPM)
        self.pedal = random.uniform(*PEDAL)

    def update(self):
        getattr(self, f"_{self.state}")()

    def _idle(self):
        self.gear = 0
        self.speed = 0.0
        self.tps = max(0.0, self.tps - 10)
        # mean reverting wander, so it drifts around idle instead of sitting on it
        self.rpm += (IDLE_RPM - self.rpm) * IDLE_SETTLE + random.uniform(
            -IDLE_HUNT, IDLE_HUNT
        )
        self.countdown -= TICK
        if self.countdown <= 0:
            self.gear = 1
            self._new_run()
            self.state = "accelerate"

    def _accelerate(self):
        self.tps = min(self.pedal, self.tps + 12)
        self._roll()
        if self.speed >= self.target:
            self.countdown = random.uniform(3, 6)
            self.state = "cruise"
        elif self.rpm >= self.shift_rpm and self.gear < len(GEAR_RATIOS):
            self.gear += 1
            self.countdown = 0.3  # time spent off throttle changing gear
            self.state = "shift"

    def _shift(self):
        self.tps = max(0.0, self.tps - 40)
        self._roll()
        self.countdown -= TICK
        if self.countdown <= 0:
            self.state = "accelerate"

    def _cruise(self):
        self.tps = max(0.0, 35.0 + random.uniform(-5, 5))
        # settle into a tall gear rather than sitting at the revs it arrived on
        while self.gear < len(GEAR_RATIOS) and self.rpm > CRUISE_RPM:
            self.gear += 1
            self.rpm = rpm_for(self.speed, self.gear)
        self._roll()
        self.countdown -= TICK
        if self.countdown <= 0:
            self.state = "brake"

    def _brake(self):
        self.tps = 0.0
        self.speed = max(0.0, self.speed - BRAKING * TICK * 3.6)
        while self.gear > 1 and rpm_for(self.speed, self.gear) < SHIFT_DOWN_RPM:
            self.gear -= 1
        self.rpm = max(IDLE_RPM, min(MAX_RPM, rpm_for(self.speed, self.gear)))
        if self.speed <= 1.0:
            self.countdown = random.uniform(1.5, 3)
            self.state = "idle"

    def _roll(self):
        """Move the car on one tick, then read the revs off the gearing"""
        speed_ms = self.speed / 3.6
        pull = GEAR_PULL[self.gear] * (self.tps / 100)
        speed_ms = max(0.0, speed_ms + (pull - DRAG * speed_ms**2) * TICK)
        self.speed = speed_ms * 3.6
        self.rpm = max(IDLE_RPM, min(MAX_RPM, rpm_for(self.speed, self.gear)))

    def write_to(self, data0):
        """Encode into the raw bytes a K-Pro v4 would have produced"""
        raw_rpm = int(self.rpm * 4)  # the backend multiplies by 0.25
        data0[constants.KPRO4_RPM1] = raw_rpm % 256
        data0[constants.KPRO4_RPM2] = min(255, raw_rpm // 256)
        data0[constants.KPRO4_VSS] = min(255, int(self.speed))
        data0[constants.KPRO4_TPS] = int(21 + self.tps * (229 - 21) / 100)
        data0[constants.KPRO4_GEAR] = self.gear


backend = Backend()
backend.ecu.ecu = Kpro()
backend.ecu.ecu.status = True
backend.ecu.ecu.version = 4
backend.ecu.ecu.data0 = [0 for _ in range(38)]
backend.ecu.ecu.data1 = [0 for _ in range(7)]
backend.ecu.ecu.data3 = [0 for _ in range(100)]
backend.ecu.ecu.data4 = [0 for _ in range(18)]
backend.ecu.ecu.data5 = [0 for _ in range(20)]

car = Car()

while True:
    # everything that is not speed, revs, throttle or gear keeps sweeping the
    # whole byte range so the rest of the gauges still move
    numbers = range(255)
    numbers = numbers if bool(random.getrandbits(1)) else reversed(numbers)
    for number in numbers:
        backend.ecu.ecu.data0 = [number for _ in range(38)]
        backend.ecu.ecu.data1 = [number for _ in range(7)]
        backend.ecu.ecu.data3 = [number for _ in range(100)]
        backend.ecu.ecu.data4 = [number for _ in range(18)]
        backend.ecu.ecu.data5 = [number for _ in range(20)]
        backend.ecu.ecu.data3[constants.KPRO4_AN0_1] = 121
        backend.ecu.ecu.data3[constants.KPRO4_AN0_2] = 121

        car.update()
        car.write_to(backend.ecu.ecu.data0)

        sleep(TICK)
