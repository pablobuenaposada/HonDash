import pytest

from backend.devices.formula import Formula


class TestFormula:
    @staticmethod
    @pytest.mark.parametrize(
        "adc, voltage", ((0, 0), (2047, 2.4993894993894994), (2047.5, 2.5), (4095, 5))
    )
    def test_adc_to_volts(adc, voltage):
        assert Formula.adc_to_volts(adc) == voltage

    @staticmethod
    @pytest.mark.parametrize("psi, bar", ((0, 0), (1, 0.0689476), (2, 0.1378952)))
    def test_psi_to_bar(psi, bar):
        assert Formula.psi_to_bar(psi) == bar

    @staticmethod
    @pytest.mark.parametrize("voltage, result", ((0, 0), (2.5, 2.5), (5, 5)))
    def test_voltage(voltage, result):
        assert Formula.voltage(voltage) == result

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, celsius, fahrenheit",
        (
            (0, 205.7905145, 402.4229261),
            (2.5, 104.39116301449056, 219.90409342608302),
            (5, -36.1485057511554, -33.067310352079716),
        ),
    )
    def test_vdo_323_057(voltage, celsius, fahrenheit):
        assert Formula.vdo_323_057(voltage) == {
            "celsius": celsius,
            "fahrenheit": fahrenheit,
        }

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, celsius, fahrenheit",
        (
            (0, 149.2065268, 300.57174824000003),
            (2.5, 76.19333584048081, 169.14800451286547),
            (5, -43.262274013110414, -45.87209322359875),
        ),
    )
    def test_aem_30_2012(voltage, celsius, fahrenheit):
        assert Formula.aem_30_2012(voltage) == {
            "celsius": celsius,
            "fahrenheit": fahrenheit,
        }

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, psi",
        ((0.5, 0.0), (2.5, 50.0), (4.5, 100.0)),
    )
    def test_autometer_2246(voltage, psi):
        """
        https://www.autometer.com/sensor_specs
        100 psi fluid pressure transducer sensor, could be also known as ebay 100 psi
        0 psi = 0.5v
        100 psi = 4.5v
        """
        assert Formula.custom(voltage, 0.5, 4.5, 0, 100) == psi

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, psi",
        ((0.5, 0.0), (2.5, 75.0), (4.5, 150.0)),
    )
    def test_ebay_150_psi(voltage, psi):
        """
        150 psi fluid pressure transducer sensor
        0 psi = 0.5v
        150 psi = 4.5v
        """
        assert Formula.custom(voltage, 0.5, 4.5, 0, 150) == psi

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, psi",
        ((0.5, 0.0), (2.5, 15.0), (4.5, 30.0)),
    )
    def test_ebay_30_psi(voltage, psi):
        """
        30 psi fluid pressure transducer sensor
        0 psi = 0.5v
        30 psi = 4.5v
        """
        assert Formula.custom(voltage, 0.5, 4.5, 0, 30) == psi

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        (
            (3.313, 0),
            (1.72, 50),
            (0.172, 100),
        ),
    )
    def test_civic_eg_fuel_tank(voltage, level):
        """
        Specs of this tank
        Empty: 110 ohms
        Full: 2 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 3.313, 0.172, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        (
            (3.292, 0),
            (1.77, 50),
            (0.294, 100),
        ),
    )
    def test_civic_ek_fuel_tank(voltage, level):
        """
        Specs of this tank
        Empty: 108 ohms
        Full: 3.5 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 3.292, 0.294, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((3.5, 0), (2.15, 50), (0.81, 100)),
    )
    def test_s2000_fuel_tank(voltage, level):
        """
        Specs of this tank
        Empty: 11 ohms
        Full: 132 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 3.51, 0.82, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((3.31, 0), (1.77, 50), (0.24, 100)),
    )
    def test_mx5_na_fuel_tank(voltage, level):
        """
        Specs of this tank (https://www.manualslib.com/download/814242/Mazda-Mx-5.html
        Empty: 110 ohms
        Full: 3 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 3.313, 0.254, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize("voltage, level", ((3.87, 0), (1.1, 100)))
    def test_mr2_w30_fuel_tank(voltage, level):
        """
        Specs of this tank (http://www.testroete.com/car/Toyota/mr2%20spyder/Repair%20Information/Repair%20Manual/
        20%20-%20Body%20Electrical/21%20-%20Combination%20Meter%20-%20Inspection.pdf)
        Empty: 192 ohms
        Full: 16 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 3.87, 1.111, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((3.31, 0), (1.77, 50), (0.24, 100)),
    )
    def test_mr2_w20_fuel_tank(voltage, level):
        """
        Specs of this tank (http://mr2.ie/mr2/bgb/mk2/mechanical/6_015.html)
        Empty: 110 ohms
        Full: 3 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 3.313, 0.254, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((3.51, 0), (2.15, 50), (0.82, 100)),
    )
    def test_integra_dc5_fuel_tank(voltage, level):
        """
        Specs of this tank from RSX workshop manual
        (http://www.mediafire.com/file/dwm2qkmzy2n/%2528LINKED_Edition%252902-06_Acura_RSX_Shop_Manual.pdf/file)
        Empty: 132 ohms
        Full: 11 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 3.510, 0.82, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((4.669, 0), (2.95, 50), (1.25, 100)),
    )
    def test_accord_cl9_fuel_tank(voltage, level):
        """
        Specs of this tank from TSX workshop manual
        (http://www.hondahookup.com/forums/downloads.php?do=file&id=158)
        Empty: 790 ohms
        Full: 19 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        assert int(Formula.custom(voltage, 4.669, 1.266, 0, 100)) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, celsius, fahrenheit",
        (
            (4.314974654, -9.999999950263089, 14.000000089526441),
            (3.128742515, 20.00000004692245, 68.00000008446042),
            (0.887030436, 80.0000000417703, 176.00000007518656),
        ),
    )
    def test_bosch_0280130039_0280130026(voltage, celsius, fahrenheit):
        assert Formula.bosch_0280130039_0280130026(voltage) == {
            "celsius": celsius,
            "fahrenheit": fahrenheit,
        }

    @staticmethod
    @pytest.mark.parametrize(
        "kpro_value, celsius, fahrenheit",
        (
            (255, -40, -40),
            (234, -17, 1),
            (225, -11, 13),
            (200, 2, 35),
            (181, 11, 51),
            (159, 22, 72),
            (140, 31, 88),
            (110, 42, 108),
            (87, 49, 121),
            (51, 69, 156),
            (40, 80, 175),
            (35, 85, 186),
            (31, 91, 195),
            (27, 96, 205),
            (24, 101, 213),
            (14, 118, 245),
            (0, 150, 303),
        ),
    )
    def test_kpro_temp(kpro_value, celsius, fahrenheit):
        assert Formula.kpro_temp(kpro_value) == {
            "celsius": celsius,
            "fahrenheit": fahrenheit,
        }

    @staticmethod
    @pytest.mark.parametrize(
        "min_voltage, max_voltage, min_value, max_value, test_value, expected_value",
        (
            (0, 0, 0, 0, 0, 0),
            (0, 5, 0, 100, 0, 0),
            (0, 5, 0, 100, 2.5, 50),
            (0, 5, 0, 100, 5, 100),
            (0, 5, 100, 0, 0, 100),
            (0, 5, 100, 0, 2.5, 50),
            (0, 5, 100, 0, 5, 0),
            (5, 0, 0, 100, 0, 100),
            (5, 0, 0, 100, 2.5, 50),
            (5, 0, 0, 100, 5, 0),
            (5, 0, 100, 0, 0, 0),
            (5, 0, 100, 0, 2.5, 50),
            (5, 0, 100, 0, 5, 100),
            (0, 5, 0, 100, 5.1, 102.0),
        ),
    )
    def test_custom(
        min_voltage, max_voltage, min_value, max_value, test_value, expected_value
    ):
        assert (
            Formula.custom(test_value, min_voltage, max_voltage, min_value, max_value)
            == expected_value
        )
