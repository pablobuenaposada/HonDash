from unittest import TestCase

from devices.formula import Formula


class TestFormula(TestCase):

    def test_vdo_323_057(self):
        self.assertEquals(Formula.vdo_323_057(0), {'celsius': 205.7905145, 'fahrenheit': 402.4229261})
        self.assertEquals(Formula.vdo_323_057(2.5), {'celsius': 104.39116301449056, 'fahrenheit': 219.90409342608302})
        self.assertEquals(Formula.vdo_323_057(5), {'fahrenheit': -33.067310352079716, 'celsius': -36.1485057511554})

    def test_aem_30_2012(self):
        self.assertEquals(Formula.aem_30_2012(0), {'celsius': 149.2065268, 'fahrenheit': 300.57174824000003})
        self.assertEquals(Formula.aem_30_2012(2.5), {'fahrenheit': 169.14800451286547, 'celsius': 76.19333584048081})
        self.assertEquals(Formula.aem_30_2012(5), {'celsius': -43.262274013110414, 'fahrenheit': -45.87209322359875})

    def test_autometer_2246(self):
        self.assertEquals(Formula.autometer_2246(0.5), {'bar': 0.0, 'psi': 0.0})
        self.assertEquals(Formula.autometer_2246(2.5), {'bar': 3.44738, 'psi': 50.0})
        self.assertEquals(Formula.autometer_2246(4.5), {'bar': 6.89476, 'psi': 100.0})

    def test_ebay_150_psi(self):
        self.assertEquals(Formula.ebay_150_psi(0.5), {'psi': 0.0, 'bar': 0.0})
        self.assertEquals(Formula.ebay_150_psi(2.5), {'psi': 75.0, 'bar': 5.17107})
        self.assertEquals(Formula.ebay_150_psi(4.5), {'bar': 10.34214, 'psi': 150.0})

    def test_adc_to_volts(self):
        self.assertEquals(Formula.adc_to_volts(0), 0)
        self.assertEquals(Formula.adc_to_volts(2047.5), 2.5)
        self.assertEquals(Formula.adc_to_volts(4095), 5)

    def test_psi_to_bar(self):
        self.assertEquals(Formula.psi_to_bar(0), 0)
        self.assertEquals(Formula.psi_to_bar(1), 0.0689476)
        self.assertEquals(Formula.psi_to_bar(2), 0.1378952)

    def test_civic_eg_fuel_tank(self):
        self.assertEquals(Formula.civic_eg_fuel_tank(3.313253012), {'per cent': 0})
        self.assertEquals(Formula.civic_eg_fuel_tank(1.836158192), {'per cent': 50})
        self.assertEquals(Formula.civic_eg_fuel_tank(0.1724137931), {'per cent': 100})

    def test_s2000_fuel_tank(self):
        self.assertEquals(Formula.s2000_fuel_tank(3.5), {'per cent': 0})
        self.assertEquals(Formula.s2000_fuel_tank(2.47), {'per cent': 50})
        self.assertEquals(Formula.s2000_fuel_tank(0.9), {'per cent': 100})
