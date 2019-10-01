import datetime

from devices.setup_file import SetupFile


class Odometer:
    def __init__(self):
        self.lastTime = datetime.datetime.now()
        self.lastSpeed = 0
        self.mileage = 0
        self.last_mileage_stored = 0
        self.setup_file = SetupFile()

        try:
            self.mileage = self.setup_file.get_value("odo").get("value")
        except AttributeError:
            pass
        self.last_mileage_stored = self.mileage

    def save(self, speed):
        """
        speed always in kmh
        """
        now = datetime.datetime.now()
        diff = (now - self.lastTime).microseconds + (
            now - self.lastTime
        ).seconds * 1000000
        km_traveled = (speed / 3600000000.0) * diff
        self.lastTime = now
        self.lastSpeed = speed
        self.mileage += km_traveled

        if (
            int(self.mileage) > self.last_mileage_stored
        ):  # only store when we ran one km more
            self.setup_file.update_key("odo", {"value": int(self.mileage)})
            self.last_mileage_stored = int(self.mileage)

    def get_mileage(self):
        return {"km": int(self.mileage), "miles": int(self.mileage * 0.6214)}
