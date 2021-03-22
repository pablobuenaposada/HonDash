import json
from json.decoder import JSONDecodeError

from backend.devices.formula import Formula

DEFAULT_CONFIG_FILE_NAME = "default_setup.json"
FILE_NAME = "setup.json"
OS_CONFIG_FILE = "/boot/config.txt"


class SetupFile:
    def __init__(self, file_name=None):
        self.file_name = file_name or FILE_NAME
        with open(self.file_name) as file:
            try:
                self.json = json.load(file)
            except JSONDecodeError:  # if there's a problem within the file let's load the default setup
                self.reset_setup()

    def get_value(self, key):
        return self.json.get(key)

    def update_key(self, key, value):
        """Update only the selected key from the setup"""
        self.json.get(key).update(value)
        self.save_setup(self.json)

    def get_formula(self, value):
        try:
            formula = self.json.get(value).get("formula")
        except AttributeError:  # if value does not exist
            formula = "voltage"

        if formula is None:  # value exists but no formula found
            formula = "voltage"

        if formula == "custom":
            extra_params = {
                "min_voltage": self.json.get(value).get("min_voltage"),
                "max_voltage": self.json.get(value).get("max_voltage"),
                "min_value": self.json.get(value).get("min_value"),
                "max_value": self.json.get(value).get("max_value"),
            }
        else:
            extra_params = None

        return getattr(Formula, formula), extra_params

    def load_setup(self, file_name=None):
        file_name = file_name or self.file_name
        with open(file_name) as file:
            self.json = json.load(file)
        return self.json

    def save_setup(self, setup):
        """Overwrite setup file"""
        with open(self.file_name, "w") as file:
            json.dump(setup, file, indent=2, sort_keys=True)
        self.__init__(self.file_name)

    def reset_setup(self):
        setup = self.load_setup(DEFAULT_CONFIG_FILE_NAME)
        self.save_setup(setup)
        self.rotate_screen(False)

    @staticmethod
    def rotate_screen(enable):
        try:
            if enable:
                if "display_rotate" not in open(OS_CONFIG_FILE).read():
                    with open(OS_CONFIG_FILE, "a+") as file:
                        file.write("display_rotate=2\n")
            else:
                if "display_rotate" in open(OS_CONFIG_FILE).read():
                    with open(OS_CONFIG_FILE, "r") as f:
                        lines = f.readlines()
                    with open(OS_CONFIG_FILE, "w") as f:
                        for line in lines:
                            if (
                                "display_rotate" not in line
                            ):  # this is just for not writing the rotate line
                                f.write(line)
        except FileNotFoundError:
            pass
