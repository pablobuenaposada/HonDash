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
    @pytest.mark.parametrize(
        "voltage, result", ((0, {"volts": 0}), (2.5, {"volts": 2.5}), (5, {"volts": 5}))
    )
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
        "voltage, bar, psi",
        ((0.5, 0.0, 0.0), (2.5, 3.44738, 50.0), (4.5, 6.89476, 100.0)),
    )
    def test_autometer_2246(voltage, bar, psi):
        assert Formula.autometer_2246(voltage) == {"bar": bar, "psi": psi}

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, bar, psi",
        ((0.5, 0.0, 0.0), (2.5, 5.17107, 75.0), (4.5, 10.34214, 150.0)),
    )
    def test_ebay_150_psi(voltage, bar, psi):
        assert Formula.ebay_150_psi(voltage) == {"bar": bar, "psi": psi}

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        (
            (3.313253012, {"per cent": 0}),
            (1.836158192, {"per cent": 50}),
            (0.1724137931, {"per cent": 100}),
        ),
    )
    def test_civic_eg_fuel_tank(voltage, level):
        assert Formula.civic_eg_fuel_tank(voltage) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        (
            (3.292682927, {"per cent": 0}),
            (1.836158192, {"per cent": 50}),
            (0.294117647, {"per cent": 100}),
        ),
    )
    def test_civic_ek_fuel_tank(voltage, level):
        assert Formula.civic_ek_fuel_tank(voltage) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((3.5, {"per cent": 0}), (2.47, {"per cent": 50}), (0.9, {"per cent": 100})),
    )
    def test_s2000_fuel_tank(voltage, level):
        assert Formula.s2000_fuel_tank(voltage) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((3.14, {"per cent": 0}), (1.85, {"per cent": 50}), (0.55, {"per cent": 100})),
    )
    def test_mx5_na_fuel_tank(voltage, level):
        assert Formula.mx5_na_fuel_tank(voltage) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level", ((1.13, {"per cent": 0}), (3.9, {"per cent": 100}))
    )
    def test_mr2_w30_fuel_tank(voltage, level):
        assert Formula.mr2_w30_fuel_tank(voltage) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level", ((3.31, {"per cent": 0}), (0.24, {"per cent": 100}))
    )
    def test_mr2_w20_fuel_tank(voltage, level):
        assert Formula.mr2_w20_fuel_tank(voltage) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((3.51, {"per cent": 0}), (2.15, {"per cent": 50}), (0.82, {"per cent": 100})),
    )
    def test_integra_dc5_fuel_tank(voltage, level):
        assert Formula.integra_dc5_fuel_tank(voltage) == level

    @staticmethod
    @pytest.mark.parametrize(
        "voltage, level",
        ((4.669, {"per cent": 0}), (2.95, {"per cent": 50}), (1.25, {"per cent": 100})),
    )
    def test_accord_cl9_fuel_tank(voltage, level):
        assert Formula.accord_cl9_fuel_tank(voltage) == level

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
