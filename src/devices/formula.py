class Formula:

    def adc_to_volts(adc):
        return (adc / 4095.000) * 5.0

    def psi_to_bar(psi):
        return psi * 0.0689476

    # VDO 323-057 sensor powered by 5v and a 56ohms voltage divider
    def vdo_323_057(volts):
        return - 6.556773822 * pow(10, -1) * pow(volts, 9) + 16.2933761 * pow(volts, 8) - 173.9768837 * pow(volts, 7) \
               + 1044.151731 * pow(volts, 6) - 3868.010224 * pow(volts, 5) + 9139.591176 * pow(volts, 4) \
               - 13733.10194 * pow(volts, 3) + 12638.52233 * pow(volts, 2) - 6520.045818 * volts + 1620.527214

    # AEM 30-2012 / Delphi 12160855 sensor powered by 5v and a 1500ohms voltage divider
    def aem_30_2012(volts):
        return - 9.800565802 * pow(10, -2) * pow(volts, 10) + 2.47857492 * pow(volts, 9) - 27.05872375 * pow(volts, 8) \
               + 167.0212269 * pow(volts, 7) - 641.3215599 * pow(volts, 6) + 1587.480011 * pow(volts, 5) \
               - 2536.694771 * pow(volts, 4) + 2537.216736 * pow(volts, 3) - 1457.917408 * pow(volts, 2) \
               + 342.4844189 * volts + 149.2065268

    # Autometer #2246 (4590-0023-12) 100 psi oil pressure sensor or ebay 100 psi
    def autometer_2246(volts):
        return 25 * volts - 12.5

    # ebay 150 psi oil pressure sensor
    def ebay_150_psi(volts):
        return 37.5 * volts - 18.75

    # civic eg fuel tank powered by 5v and a 1500ohms voltage divider
    def civic_eg_fuel_tank(volts):
        return int(868.427437 * pow(volts, 2) - 600.9952442 * volts + 103.9628058)

    # s2000 fuel tank powered by 5v and a 1500ohms voltage divider
    def s2000_fuel_tank(volts):
        return int(425.3064645 * pow(volts, 2) - 466.933388 * volts + 119.2749615)
