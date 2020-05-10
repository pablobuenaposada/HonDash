import datetime

from backend.devices.setup_file import SetupFile


class Odometer:
    def __init__(self):
        self.lastTime = datetime.datetime.now()
        self.lastSpeed = 0
        self.mileage = 0  # always stored in km
        self.last_mileage_stored = 0
        setup_file = SetupFile()

        try:
            self.mileage = setup_file.get_value("odo").get("value")
            unit = setup_file.get_value("odo").get("unit")
            if unit == "miles":  # if mileage is in miles let's convert it to km
                self.mileage = self._miles_to_km(self.mileage)
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
            setup_file = SetupFile()
            setup_file.update_key("odo", {"value": int(self.mileage)})
            self.last_mileage_stored = int(self.mileage)

    def get_mileage(self):
        return {"km": int(self.mileage), "miles": self._km_to_miles(self.mileage)}

    @staticmethod
    def _km_to_miles(km):
        return int(km * 0.6214)

    @staticmethod
    def _miles_to_km(miles):
        return int(miles * 1.609)
