import json

from devices.formula import Formula


class Mapper:
    def __init__(self):
        with open('mapping.json') as file:
            self.map = json.load(file)

    def get_unit(self, value):
        try:
            return self.map.get(value).get('unit')
        except AttributeError:
            return None

    def get_formula(self, value):
        try:
            formula = self.map.get(value).get('formula')
        except AttributeError:  # if value does not exist
            formula = 'voltage'

        if formula is None:  # value exists but no formula found
            formula = 'voltage'

        return getattr(Formula, formula)
