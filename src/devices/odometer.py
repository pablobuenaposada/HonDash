import datetime
from atomicwrites import atomic_write


class Odometer:
    def __init__(self):
        self.lastTime = datetime.datetime.now()
        self.lastSpeed = 0
        self.mileage = 0
        self.last_mileage_stored = 0

        try:
            f = open('odometer.txt', 'r')
            self.mileage = int(f.read())
        except OSError:
            pass
        self.last_mileage_stored = self.mileage

    def save(self, speed):
        now = datetime.datetime.now()
        diff = (now - self.lastTime).microseconds + (now - self.lastTime).seconds * 1000000
        km_traveled = (speed / 3600000000.0) * diff
        self.lastTime = now
        self.lastSpeed = speed
        self.mileage += km_traveled

        if int(self.mileage) > self.last_mileage_stored:  # only store when we ran one km more
            with atomic_write('odometer.txt', overwrite=True) as f:
                f.write(str(int(self.mileage)))
                self.last_mileage_stored = int(self.mileage)

    def get_mileage(self):
        return int(self.mileage)
