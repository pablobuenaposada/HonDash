class Formula:

    # Backup formula method to use when no formula is found
    @staticmethod
    def voltage(value):
        return {"volts": value}

    @staticmethod
    def adc_to_volts(adc):
        return (adc / 4095.000) * 5.0

    @staticmethod
    def psi_to_bar(psi):
        return psi * 0.0689476

    @staticmethod
    def bar_to_psi(bar):
        return bar * 14.503773773

    @staticmethod
    def kmh_to_mph(kmh):
        return kmh * 0.6214

    @staticmethod
    def celsius_to_fahrenheit(celsius):
        return (celsius * 1.8) + 32

    @staticmethod
    def kpro_temp(kpro_value):
        """
        Conversion of whatever temperature unit kpro outputs into celsius and fahrenheit units.
        Linear regression made with https://arachnoid.com/polysolve/
        """
        celsius = (
            -2.7168631716148286 * pow(10, 0) * kpro_value
            + 3.5250001884568352 * pow(10, -2) * pow(kpro_value, 2)
            - 4.6668312213461976 * pow(10, -4) * pow(kpro_value, 3)
            + 6.2314622546038854 * pow(10, -6) * pow(kpro_value, 4)
            - 5.5155685454381802 * pow(10, -8) * pow(kpro_value, 5)
            + 2.6888773098684158 * pow(10, -10) * pow(kpro_value, 6)
            - 6.5904712075799765 * pow(10, -13) * pow(kpro_value, 7)
            + 6.3467552343485511 * pow(10, -16) * pow(kpro_value, 8)
            + 1.5037636674235824 * pow(10, 2)
        )
        return {
            "celsius": round(celsius),
            "fahrenheit": round(Formula.celsius_to_fahrenheit(celsius)),
        }

    # VDO 323-057 sensor powered by 5v and a 56ohms voltage divider
    @staticmethod
    def vdo_323_057(volts):
        celsius = (
            -2.183715894 * pow(10, -1) * pow(volts, 10)
            + 5.613288037 * pow(volts, 9)
            - 62.2205559 * pow(volts, 8)
            + 389.2848412 * pow(volts, 7)
            - 1510.989619 * pow(volts, 6)
            + 3764.608696 * pow(volts, 5)
            - 6013.228539 * pow(volts, 4)
            + 5943.529221 * pow(volts, 3)
            - 3309.957466 * pow(volts, 2)
            + 750.5177822 * volts
            + 205.7905145
        )
        return {
            "celsius": celsius,
            "fahrenheit": Formula.celsius_to_fahrenheit(celsius),
        }

    # AEM 30-2012 / Delphi 12160855 sensor powered by 5v and a 1500ohms voltage divider
    @staticmethod
    def aem_30_2012(volts):
        celsius = (
            -9.800565802 * pow(10, -2) * pow(volts, 10)
            + 2.47857492 * pow(volts, 9)
            - 27.05872375 * pow(volts, 8)
            + 167.0212269 * pow(volts, 7)
            - 641.3215599 * pow(volts, 6)
            + 1587.480011 * pow(volts, 5)
            - 2536.694771 * pow(volts, 4)
            + 2537.216736 * pow(volts, 3)
            - 1457.917408 * pow(volts, 2)
            + 342.4844189 * volts
            + 149.2065268
        )
        return {
            "celsius": celsius,
            "fahrenheit": Formula.celsius_to_fahrenheit(celsius),
        }

    # Bosch 0280130039 / 0280130026 sensor powered by 5v and a 1500ohms voltage divider
    @staticmethod
    def bosch_0280130039_0280130026(volts):
        celsius = (
            4.303155022 * pow(10, -1) * pow(volts, 2)
            - 28.49330639 * volts
            + 104.9358479
        )
        return {
            "celsius": celsius,
            "fahrenheit": Formula.celsius_to_fahrenheit(celsius),
        }

    # Autometer #2246 (4590-0023-12) 100 psi oil pressure sensor or ebay 100 psi
    @staticmethod
    def autometer_2246(volts):
        psi = 25 * volts - 12.5
        return {"psi": psi, "bar": Formula.psi_to_bar(psi)}

    # ebay 150 psi oil pressure sensor
    @staticmethod
    def ebay_150_psi(volts):
        psi = 37.5 * volts - 18.75
        return {"psi": psi, "bar": Formula.psi_to_bar(psi)}

    # civic eg fuel tank powered by 5v and a 56ohms voltage divider
    @staticmethod
    def civic_eg_fuel_tank(volts):
        return {
            "per cent": int(
                -1.209083604 * pow(volts, 2) - 27.62416175 * volts + 104.7987284
            )
        }

    @staticmethod
    def civic_ek_fuel_tank(volts):
        """
        Specs of this tank
        Empty: 105-108 ohms
        Half: 29.5-35.5 ohms
        Full: 3.5-5 ohms
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        return {
            "per cent": int(
                -0.6348765014 * pow(volts, 2) - 31.07210689 * volts + 109.1937751
            )
        }

    # s2000 fuel tank powered by 5v and a 56ohms voltage divider
    @staticmethod
    def s2000_fuel_tank(volts):
        return {
            "per cent": int(
                -6.163413263 * pow(volts, 2) - 11.48794404 * volts + 116.2915039
            )
        }

    # toyota mr2 w30 fuel tank powered by 5v and a 56ohms voltage divider
    @staticmethod
    def mr2_w30_fuel_tank(volts):
        return {"per cent": int(36.4757313 * volts - 41.31229235)}

    # mazda mx5 na fuel tank powered by 5v and a 56ohms voltage divider
    @staticmethod
    def mx5_na_fuel_tank(volts):
        return {
            "per cent": int(
                -7.612787523 * pow(10, -2) * pow(volts, 2)
                - 38.32618618 * volts
                + 121.3158219
            )
        }
