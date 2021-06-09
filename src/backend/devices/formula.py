class Formula:

    # Backup formula method to use when no formula is found
    @staticmethod
    def voltage(value):
        return value

    @staticmethod
    def adc_to_volts(adc):
        return (adc / 4095) * 5

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

    @staticmethod
    def custom(voltage, min_voltage, max_voltage, min_value, max_value):
        """
        This function calculates the equation of the straight line given 2 points (y=mx+b), in this case we are
        gonna use the axis voltage (0-5v) and whatever other range and unit the sensor outputs
        """
        try:
            m = (min_value - max_value) / (min_voltage - max_voltage)  # slope
            b = (min_voltage * max_value - max_voltage * min_value) / (
                min_voltage - max_voltage
            )  # Y-intercept
        except ZeroDivisionError:
            return 0
        return m * voltage + b

    @staticmethod
    def vdo_323_057(voltage):
        """
        VDO 323-057 oil temperature sensor
        Resistance used for voltage divider: 56 ohms
        Vin: 5v
        """
        celsius = (
            -2.183715894 * pow(10, -1) * pow(voltage, 10)
            + 5.613288037 * pow(voltage, 9)
            - 62.2205559 * pow(voltage, 8)
            + 389.2848412 * pow(voltage, 7)
            - 1510.989619 * pow(voltage, 6)
            + 3764.608696 * pow(voltage, 5)
            - 6013.228539 * pow(voltage, 4)
            + 5943.529221 * pow(voltage, 3)
            - 3309.957466 * pow(voltage, 2)
            + 750.5177822 * voltage
            + 205.7905145
        )
        return {
            "celsius": celsius,
            "fahrenheit": Formula.celsius_to_fahrenheit(celsius),
        }

    @staticmethod
    def aem_30_2012(voltage):
        """
        AEM 30-2012 / Delphi 12160855 oil temperature sensors
        https://www.aemelectronics.com/sites/default/files/aem_product_instructions/30-2012%20Water%20Temp%20Sensor%20Kit.pdf
        Resistance used for voltage divider: 1500 ohms
        Vin: 5v
        """
        celsius = (
            -9.800565802 * pow(10, -2) * pow(voltage, 10)
            + 2.47857492 * pow(voltage, 9)
            - 27.05872375 * pow(voltage, 8)
            + 167.0212269 * pow(voltage, 7)
            - 641.3215599 * pow(voltage, 6)
            + 1587.480011 * pow(voltage, 5)
            - 2536.694771 * pow(voltage, 4)
            + 2537.216736 * pow(voltage, 3)
            - 1457.917408 * pow(voltage, 2)
            + 342.4844189 * voltage
            + 149.2065268
        )
        return {
            "celsius": celsius,
            "fahrenheit": Formula.celsius_to_fahrenheit(celsius),
        }

    @staticmethod
    def bosch_0280130039_0280130026(voltage):
        """
        Bosch 0280130039 / 0280130026 oil temperature sensors
        For 0280130039 this are the specs:
        https://www.bosch-motorsport.com/content/downloads/Raceparts/Resources/pdf/Data%20sheet_70129803_Temperature_Sensor_NTC_M12-L.pdf
        For 0280130026 this are the specs:
        https://www.bosch-motorsport.com/content/downloads/Raceparts/Resources/pdf/Data%20sheet_70101387_Temperature_Sensor_NTC_M12.pdf
        The specs are the same for both
        Resistance used for voltage divider: 1500 ohms
        Vin: 5v
        """
        celsius = (
            4.303155022 * pow(10, -1) * pow(voltage, 2)
            - 28.49330639 * voltage
            + 104.9358479
        )
        return {
            "celsius": celsius,
            "fahrenheit": Formula.celsius_to_fahrenheit(celsius),
        }
