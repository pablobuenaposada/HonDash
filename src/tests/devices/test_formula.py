from unittest import TestCase

from devices.formula import Formula


class TestFormula(TestCase):
    def test_vdo_323_057(self):
        self.assertEqual(
            Formula.vdo_323_057(0), {"celsius": 205.7905145, "fahrenheit": 402.4229261}
        )
        self.assertEqual(
            Formula.vdo_323_057(2.5),
            {"celsius": 104.39116301449056, "fahrenheit": 219.90409342608302},
        )
        self.assertEqual(
            Formula.vdo_323_057(5),
            {"fahrenheit": -33.067310352079716, "celsius": -36.1485057511554},
        )

    def test_aem_30_2012(self):
        self.assertEqual(
            Formula.aem_30_2012(0),
            {"celsius": 149.2065268, "fahrenheit": 300.57174824000003},
        )
        self.assertEqual(
            Formula.aem_30_2012(2.5),
            {"fahrenheit": 169.14800451286547, "celsius": 76.19333584048081},
        )
        self.assertEqual(
            Formula.aem_30_2012(5),
            {"celsius": -43.262274013110414, "fahrenheit": -45.87209322359875},
        )

    def test_autometer_2246(self):
        self.assertEqual(Formula.autometer_2246(0.5), {"bar": 0.0, "psi": 0.0})
        self.assertEqual(Formula.autometer_2246(2.5), {"bar": 3.44738, "psi": 50.0})
        self.assertEqual(Formula.autometer_2246(4.5), {"bar": 6.89476, "psi": 100.0})

    def test_ebay_150_psi(self):
        self.assertEqual(Formula.ebay_150_psi(0.5), {"psi": 0.0, "bar": 0.0})
        self.assertEqual(Formula.ebay_150_psi(2.5), {"psi": 75.0, "bar": 5.17107})
        self.assertEqual(Formula.ebay_150_psi(4.5), {"bar": 10.34214, "psi": 150.0})

    def test_adc_to_volts(self):
        self.assertEqual(Formula.adc_to_volts(0), 0)
        self.assertEqual(Formula.adc_to_volts(2047.5), 2.5)
        self.assertEqual(Formula.adc_to_volts(4095), 5)

    def test_psi_to_bar(self):
        self.assertEqual(Formula.psi_to_bar(0), 0)
        self.assertEqual(Formula.psi_to_bar(1), 0.0689476)
        self.assertEqual(Formula.psi_to_bar(2), 0.1378952)

    def test_civic_eg_fuel_tank(self):
        self.assertEqual(Formula.civic_eg_fuel_tank(3.313253012), {"per cent": 0})
        self.assertEqual(Formula.civic_eg_fuel_tank(1.836158192), {"per cent": 50})
        self.assertEqual(Formula.civic_eg_fuel_tank(0.1724137931), {"per cent": 100})

    def test_civic_ek_fuel_tank(self):
        self.assertEqual(Formula.civic_ek_fuel_tank(3.292682927), {"per cent": 0})
        self.assertEqual(Formula.civic_ek_fuel_tank(1.836158192), {"per cent": 50})
        self.assertEqual(Formula.civic_ek_fuel_tank(0.294117647), {"per cent": 100})

    def test_s2000_fuel_tank(self):
        self.assertEqual(Formula.s2000_fuel_tank(3.5), {"per cent": 0})
        self.assertEqual(Formula.s2000_fuel_tank(2.47), {"per cent": 50})
        self.assertEqual(Formula.s2000_fuel_tank(0.9), {"per cent": 100})

    def test_mx5_na_fuel_tank(self):
        self.assertEqual(Formula.mx5_na_fuel_tank(3.14), {"per cent": 0})
        self.assertEqual(Formula.mx5_na_fuel_tank(1.85), {"per cent": 50})
        self.assertEqual(Formula.mx5_na_fuel_tank(0.55), {"per cent": 100})

    def test_mr2_w30_fuel_tank(self):
        self.assertEqual(Formula.mr2_w30_fuel_tank(1.13), {"per cent": 0})
        self.assertEqual(Formula.mr2_w30_fuel_tank(3.9), {"per cent": 100})

    def test_bosch_0280130039_0280130026(self):
        self.assertEqual(
            Formula.bosch_0280130039_0280130026(4.314974654),
            {"celsius": -9.999999950263089, "fahrenheit": 14.000000089526441},
        )
        self.assertEqual(
            Formula.bosch_0280130039_0280130026(3.128742515),
            {"celsius": 20.00000004692245, "fahrenheit": 68.00000008446042},
        )
        self.assertEqual(
            Formula.bosch_0280130039_0280130026(0.887030436),
            {"celsius": 80.0000000417703, "fahrenheit": 176.00000007518656},
        )
