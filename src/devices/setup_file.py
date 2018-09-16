import json

from devices.formula import Formula

FILE_NAME = 'setup.json'


class SetupFile:
    def __init__(self):
        with open(FILE_NAME) as file:
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
        with open(FILE_NAME) as file:
            self.json = json.load(file)
        return self.json

    def save_setup(self, setup):
        with open(FILE_NAME, 'w') as file:
            json.dump(setup, file, indent=2)
