from unittest import TestCase

from backend.mapper import Mapper

from devices.formula import Formula


class TestMapper(TestCase):
    def setUp(self):
        self.mapper = Mapper()

    def test_get_unit(self):
        self.assertEquals(self.mapper.get_unit('vss'), 'kmh')
        self.assertEquals(self.mapper.get_unit('foo'), None)

    def test_get_formula(self):
        self.assertEquals(self.mapper.get_formula('an0'), Formula.ebay_150_psi)
        self.assertEquals(self.mapper.get_formula('foo'), Formula.voltage)

    def test_get_setup(self):
        print(self.mapper.get_setup())
