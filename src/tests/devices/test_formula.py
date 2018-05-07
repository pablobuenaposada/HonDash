from unittest import TestCase

from devices.formula import Formula


class TestFormula(TestCase):

    def test_vdo_323_057(self):
        self.assertEquals(Formula.vdo_323_057(0), 1620.527214)
        self.assertEquals(Formula.vdo_323_057(2.5), 104.66787557340672)
        self.assertEquals(Formula.vdo_323_057(5), -34.94136037743533)

    def test_autometer_2246(self):
        self.assertEquals(Formula.autometer_2246(0.5), 0)
        self.assertEquals(Formula.autometer_2246(2.5), 50)
        self.assertEquals(Formula.autometer_2246(4.5), 100)

    def test_ebay_150_psi(self):
        self.assertEquals(Formula.ebay_150_psi(0.5), 0)
        self.assertEquals(Formula.ebay_150_psi(2.5), 75)
        self.assertEquals(Formula.ebay_150_psi(4.5), 150)

    def test_adc_to_volts(self):
        self.assertEquals(Formula.adc_to_volts(0), 0)
        self.assertEquals(Formula.adc_to_volts(2047.5), 2.5)
        self.assertEquals(Formula.adc_to_volts(4095), 5)

    def test_psi_to_bar(self):
        self.assertEquals(Formula.psi_to_bar(0), 0)
        self.assertEquals(Formula.psi_to_bar(1), 0.0689476)
        self.assertEquals(Formula.psi_to_bar(2), 0.1378952)

    def test_civic_eg_fuel_tank(self):
        self.assertEquals(int(Formula.civic_eg_fuel_tank(3.313253012)), 0)
        self.assertEquals(int(Formula.civic_eg_fuel_tank(1.836158192)), 50)
        self.assertEquals(int(Formula.civic_eg_fuel_tank(0.1724137931)), 100)
