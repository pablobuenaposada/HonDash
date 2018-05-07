class Formula:

    def adc_to_volts(adc):
        return (adc / 4095.000) * 5.0

    def psi_to_bar(psi):
        return psi * 0.0689476

    # VDO 323-057 sensor powered by 5v and a 56ohms voltage divider
    def vdo_323_057(volts):
        return -6.556773822 * pow(10, -1) * pow(volts, 9) + 16.2933761 * pow(volts, 8) - 173.9768837 * pow(volts, 7) \
               + 1044.151731 * pow(volts, 6) - 3868.010224 * pow(volts, 5) + 9139.591176 * pow(volts, 4) \
               - 13733.10194 * pow(volts, 3) + 12638.52233 * pow(volts, 2) - 6520.045818 * volts + 1620.527214

    # Autometer #2246 (4590-0023-12) 100 psi oil pressure sensor or ebay 100 psi
    def autometer_2246(volts):
        return 25 * volts - 12.5

    # ebay 150 psi oil pressure sensor
    def ebay_150_psi(volts):
        return 37.5 * volts - 18.75

    def civic_eg_fuel_tank(volts):
        return int(-1.209083604 * pow(volts, 2) - 27.62416175 * volts + 104.7987284)
