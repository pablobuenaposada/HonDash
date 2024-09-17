from constants import websocket_data_dict
from devices.ecu import Ecu
from devices.logger.logger import Logger
from devices.odometer import Odometer
from devices.setup_file import SetupFile
from devices.setup_validator.setup_validator import SetupValidator
from devices.style import Style
from devices.time import Time
from version import __version__
from websocket import Websocket


class Backend:
    def __init__(self):
        self._load_user_preferences()
        self._init_resources()
        self._init_websocket()
        self.logger = Logger(self.setup_file.json.get("hddlg").get("autostart"))

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
        # if we are here because a reset don't re-init the ecu
        try:
            self.ecu
        except AttributeError:
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

        self.an0_formula, self.an0_extra_params = self.setup_file.get_formula("an0")
        self.an1_formula, self.an1_extra_params = self.setup_file.get_formula("an1")
        self.an2_formula, self.an2_extra_params = self.setup_file.get_formula("an2")
        self.an3_formula, self.an3_extra_params = self.setup_file.get_formula("an3")
        self.an4_formula, self.an4_extra_params = self.setup_file.get_formula("an4")
        self.an5_formula, self.an5_extra_params = self.setup_file.get_formula("an5")
        self.an6_formula, self.an6_extra_params = self.setup_file.get_formula("an6")
        self.an7_formula, self.an7_extra_params = self.setup_file.get_formula("an7")

    def _call_analog_input(self, port):
        voltage = self.ecu.analog_input(port)
        extra_params = getattr(self, f"an{port}_extra_params")
        formula = getattr(self, f"an{port}_formula")

        if extra_params is None:  # then is a specific formula
            return formula(voltage)[getattr(self, f"an{port}_unit")]
        else:
            args = {"voltage": voltage}
            args.update(extra_params)
            return formula(**args)

    def update(self):
        """load the websocket with updated info"""
        if self.odo.save(self.ecu.vss["kmh"]):
            self.setup_file.update_key("odo", {"value": self.odo.preferred_mileage})
        self.style.update(self.ecu.tps)
        return websocket_data_dict(
            self.ecu,
            self.iat_unit,
            self.ect_unit,
            self.vss_unit,
            self.o2_unit,
            self.map_unit,
            self._call_analog_input,
            self.time.get_time(),
            self.odo.preferred_mileage,
            self.style.status,
            __version__,
            self.logger,
        )

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
