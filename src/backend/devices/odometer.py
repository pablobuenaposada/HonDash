import datetime


class Odometer:
    def __init__(self, initial_mileage=0, unit="km"):
        self.lastTime = datetime.datetime.now()
        self.lastSpeed = 0
        self.mileage = initial_mileage
        self.preferred_unit = unit
        self.last_mileage_stored = 0

        if (
            self.preferred_unit == "miles"
        ):  # if mileage is in miles let's convert it to km
            self.mileage = self._miles_to_km(self.mileage)
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

        # only store when we ran one km more
        if int(self.mileage) > self.last_mileage_stored:
            self.last_mileage_stored = int(self.mileage)
            return True
        else:
            return False

    def get_mileage(self):
        return {"km": int(self.mileage), "miles": self._km_to_miles(self.mileage)}

    @property
    def preferred_mileage(self):
        return self.get_mileage()[self.preferred_unit]

    @staticmethod
    def _km_to_miles(km):
        return int(km * 0.621371)

    @staticmethod
    def _miles_to_km(miles):
        return int(miles * 1.609344)
