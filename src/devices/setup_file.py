import json

from devices.formula import Formula

FILE_NAME = 'setup.json'
OS_CONFIG_FILE = '/boot/config.txt'


class SetupFile:
    def __init__(self, file_name=FILE_NAME):
        self.file_name = file_name
        with open(self.file_name) as file:
            self.json = json.load(file)

    def get_value(self, key):
        return self.json.get(key)

    def update_key(self, key, value):
        self.json.get(key).update(value)
        self.save_setup(self.json)

    def get_formula(self, value):
        try:
            formula = self.json.get(value).get('formula')
        except AttributeError:  # if value does not exist
            formula = 'voltage'

        if formula is None:  # value exists but no formula found
            formula = 'voltage'

        return getattr(Formula, formula)

    def load_setup(self):
        with open(self.file_name) as file:
            self.json = json.load(file)
        return self.json

    def save_setup(self, setup):
        self.json.update(setup)
        with open(self.file_name, 'w') as file:
            json.dump(self.json, file, indent=2, sort_keys=True)
        self.__init__(self.file_name)

    @staticmethod
    def rotate_screen(enable):
        try:
            if enable:
                if 'display_rotate' not in open(OS_CONFIG_FILE).read():
                    with open(OS_CONFIG_FILE, "a+") as file:
                        file.write("display_rotate=2\n")
            else:
                if 'display_rotate' in open(OS_CONFIG_FILE).read():
                    with open(OS_CONFIG_FILE, "r") as f:
                        lines = f.readlines()
                    with open(OS_CONFIG_FILE, "w") as f:
                        for line in lines:
                            if 'display_rotate' not in line:
                                f.write(line)
        except FileNotFoundError:
            pass
