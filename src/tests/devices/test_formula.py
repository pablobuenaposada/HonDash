from unittest import TestCase

from src.devices.formula import Formula


class TestFormula(TestCase):

    def test_vdo_323_057(self):
        self.assertEquals(Formula.vdo_323_057(0), 1620.527214)
        self.assertEquals(Formula.vdo_323_057(2048), 104.64810848793081)
        self.assertEquals(Formula.vdo_323_057(4095), -34.94136037743533)

    def test_autometer_2246(self):
        self.assertEquals(Formula.autometer_2246(409.5), 0)
        self.assertEquals(Formula.autometer_2246(2047.5), 50)
        self.assertEquals(Formula.autometer_2246(3685.5), 100)

    def test_ebay_150_psi(self):
        self.assertEquals(Formula.ebay_150_psi(409.5), 0)
        self.assertEquals(Formula.ebay_150_psi(2047.5), 75)
        self.assertEquals(Formula.ebay_150_psi(3685.5), 150)
