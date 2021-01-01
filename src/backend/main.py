from backend.devices.ecu import Ecu
from backend.devices.odometer import Odometer
from backend.devices.setup_file import SetupFile
from backend.devices.setup_validator.setup_validator import SetupValidator
from backend.devices.style import Style
from backend.devices.time import Time
from backend.websocket import Websocket
from version import __version__


class Backend:
    def __init__(self):
        self._load_user_preferences()
        self._init_resources()
        self._init_websocket()

    def stop(self):
        self.websocket.stop()

    def _init_websocket(self):
        self.websocket = Websocket(self)

    def _init_resources(self):
        self.time = Time()
        self.odo = Odometer(
            self.setup_file.get_value("odo").get("value"),
            self.setup_file.get_value("odo").get("unit"),
        )
        self.ecu = Ecu()

    def _load_user_preferences(self):
        """
        In order to read only once from the setup file
        we will load in memory some user preferences that we are gonna use later on.
        """
        self.setup_file = SetupFile()

        self.style = Style(
            self.setup_file.json.get("style").get("tpsLowerThreshold"),
            self.setup_file.json.get("style").get("tpsUpperThreshold"),
            self.setup_file.json.get("style").get("elapsedSeconds"),
        )

        self.iat_unit = self.setup_file.json.get("iat", {}).get("unit", "celsius")
        self.ect_unit = self.setup_file.json.get("ect", {}).get("unit", "celsius")
        self.vss_unit = self.setup_file.json.get("vss", {}).get("unit", "kmh")
        self.o2_unit = self.setup_file.json.get("o2", {}).get("unit", "afr")
        self.odo_unit = self.setup_file.json.get("odo", {}).get("unit", "km")
        self.map_unit = self.setup_file.json.get("map", {}).get("unit", "bar")
        self.an0_unit = self.setup_file.json.get("an0", {}).get("unit", "volts")
        self.an1_unit = self.setup_file.json.get("an1", {}).get("unit", "volts")
        self.an2_unit = self.setup_file.json.get("an2", {}).get("unit", "volts")
        self.an3_unit = self.setup_file.json.get("an3", {}).get("unit", "volts")
        self.an4_unit = self.setup_file.json.get("an4", {}).get("unit", "volts")
        self.an5_unit = self.setup_file.json.get("an5", {}).get("unit", "volts")
        self.an6_unit = self.setup_file.json.get("an6", {}).get("unit", "volts")
        self.an7_unit = self.setup_file.json.get("an7", {}).get("unit", "volts")

        self.an0_formula = self.setup_file.get_formula("an0")
        self.an1_formula = self.setup_file.get_formula("an1")
        self.an2_formula = self.setup_file.get_formula("an2")
        self.an3_formula = self.setup_file.get_formula("an3")
        self.an4_formula = self.setup_file.get_formula("an4")
        self.an5_formula = self.setup_file.get_formula("an5")
        self.an6_formula = self.setup_file.get_formula("an6")
        self.an7_formula = self.setup_file.get_formula("an7")

    def update(self):
        """ load the websocket with updated info """
        if self.odo.save(self.ecu.vss["kmh"]):
            self.setup_file.update_key("odo", {"value": self.odo.preferred_mileage})
        self.style.update(self.ecu.tps)
        return {
            "bat": self.ecu.bat,
            "gear": self.ecu.gear,
            "iat": self.ecu.iat[self.iat_unit],
            "tps": self.ecu.tps,
            "ect": self.ecu.ect[self.ect_unit],
            "rpm": self.ecu.rpm,
            "vss": self.ecu.vss[self.vss_unit],
            "o2": self.ecu.o2[self.o2_unit],
            "cam": self.ecu.cam,
            "mil": self.ecu.mil,
            "fan": self.ecu.fanc,
            "bksw": self.ecu.bksw,
            "flr": self.ecu.flr,
            "eth": self.ecu.eth,
            "scs": self.ecu.scs,
            "fmw": self.ecu.firmware,
            "map": self.ecu.map[self.map_unit],
            "an0": self.an0_formula(self.ecu.analog_input(0))[self.an0_unit],
            "an1": self.an1_formula(self.ecu.analog_input(1))[self.an1_unit],
            "an2": self.an2_formula(self.ecu.analog_input(2))[self.an2_unit],
            "an3": self.an3_formula(self.ecu.analog_input(3))[self.an3_unit],
            "an4": self.an4_formula(self.ecu.analog_input(4))[self.an4_unit],
            "an5": self.an5_formula(self.ecu.analog_input(5))[self.an5_unit],
            "an6": self.an6_formula(self.ecu.analog_input(6))[self.an6_unit],
            "an7": self.an7_formula(self.ecu.analog_input(7))[self.an7_unit],
            "time": self.time.get_time(),
            "odo": self.odo.preferred_mileage,
            "style": self.style.status,
            "name": self.ecu.name,
            "ver": __version__,
        }

    def setup(self):
        """Return the current setup"""
        return self.setup_file.load_setup()

    def save(self, new_setup):
        """Save a new setup"""
        SetupValidator().validate(new_setup)
        self.setup_file.save_setup(new_setup)
        self.setup_file.rotate_screen(new_setup["screen"]["rotate"])
        # refresh the backend too
        self._load_user_preferences()
        self._init_resources()

    def reset(self):
        """Reset to the default setup"""
        self.setup_file.reset_setup()
        # refresh the backend too
        self._load_user_preferences()
        self._init_resources()


if __name__ == "__main__":
    # if the file is getting executed then start the backend behaviour
    backend = Backend()
