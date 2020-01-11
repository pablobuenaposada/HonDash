from time import sleep

from autobahn_sync import publish, register, run

from devices.kpro.kpro import Kpro
from devices.odometer import Odometer
from devices.setup_file import SetupFile
from devices.style import Style
from devices.time import Time
from version import __version__


@register(u"setup")
def setup():
    """ Remote Procedure Call used from the frontend """
    return Backend.setup()


@register(u"save")
def save(new_setup):
    """ Remote Procedure Call used from the frontend """
    Backend.save(new_setup)


@register(u"reset")
def reset():
    """ Remote Procedure Call used from the frontend """
    Backend.reset()


class Backend:
    _instance = None
    _resources_started = False

    def __init__(self):
        self._init_websocket()
        self._load_user_preferences()

    @staticmethod
    def _init_websocket():
        while True:
            try:
                run()
                break
            except Exception:
                pass  # don't give up mate, we have to start this thing no matter how

    def _init_resources(self):
        self.time = Time()
        self.odo = Odometer()
        self.kpro = Kpro()
        self._resources_started = self.kpro.status

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
        if not self._resources_started:
            self._init_resources()
        else:
            """ load the websocket with updated info """
            self.odo.save(self.kpro.vss()["kmh"])
            self.style.update(self.kpro.tps())
            publish(
                "data",
                {
                    "bat": self.kpro.bat(),
                    "gear": self.kpro.gear(),
                    "iat": self.kpro.iat()[self.iat_unit],
                    "tps": self.kpro.tps(),
                    "ect": self.kpro.ect()[self.ect_unit],
                    "rpm": self.kpro.rpm(),
                    "vss": self.kpro.vss()[self.vss_unit],
                    "o2": self.kpro.o2()[self.o2_unit],
                    "cam": self.kpro.cam(),
                    "mil": self.kpro.mil(),
                    "fan": self.kpro.fanc(),
                    "bksw": self.kpro.bksw(),
                    "flr": self.kpro.flr(),
                    "eth": self.kpro.eth(),
                    "scs": self.kpro.scs(),
                    "fmw": self.kpro.firmware(),
                    "map": self.kpro.map()[self.map_unit],
                    "an0": self.an0_formula(self.kpro.analog_input(0))[self.an0_unit],
                    "an1": self.an1_formula(self.kpro.analog_input(1))[self.an1_unit],
                    "an2": self.an2_formula(self.kpro.analog_input(2))[self.an2_unit],
                    "an3": self.an3_formula(self.kpro.analog_input(3))[self.an3_unit],
                    "an4": self.an4_formula(self.kpro.analog_input(4))[self.an4_unit],
                    "an5": self.an5_formula(self.kpro.analog_input(5))[self.an5_unit],
                    "an6": self.an6_formula(self.kpro.analog_input(6))[self.an6_unit],
                    "an7": self.an7_formula(self.kpro.analog_input(7))[self.an7_unit],
                    "time": self.time.get_time(),
                    "odo": self.odo.get_mileage()[self.odo_unit],
                    "style": self.style.status,
                    "ver": __version__,
                },
            )

    def _setup(self):
        return self.setup_file.load_setup()

    def _save(self, new_setup):
        self.setup_file.save_setup(new_setup)
        self.setup_file.rotate_screen(new_setup["screen"]["rotate"])
        publish("refresh")  # refresh the frontend so the new changes are applied
        self._load_user_preferences()  # refresh the backend too

    def _reset(self):
        self.setup_file.reset_setup()
        publish("refresh")  # refresh the frontend so the new changes are applied
        self._load_user_preferences()  # refresh the backend too

    @classmethod
    def get(cls):
        """ get the running instance of Backend class or instantiate it for first time """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def setup(cls):
        return cls.get()._setup()

    @classmethod
    def save(cls, new_setup):
        cls.get()._save(new_setup)

    @classmethod
    def reset(cls):
        cls.get()._reset()


if __name__ == "__main__":
    # if the file is getting executed then start the backend behaviour
    backend = Backend.get()
    while True:
        backend.update()
        sleep(0.1)  # TODO: not use sleep :(
