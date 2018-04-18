class Formula:
    # VDO 323-057 sensor powered by 5v and read with a 56ohms voltage divider
    def vdo_323_057(adc):
        volts = (adc / 4096.000) * 5.0
        return -6.556773822 * pow(10, -1) * pow(volts, 9) + 16.2933761 * pow(volts, 8) - 173.9768837 * pow(volts, 7) \
               + 1044.151731 * pow(volts, 6) - 3868.010224 * pow(volts, 5) + 9139.591176 * pow(volts, 4) \
               - 13733.10194 * pow(volts, 3) + 12638.52233 * pow(volts, 2) - 6520.045818 * volts + 1620.527214

    # Autometer #2246 (4590-0023-12) 100 psi oil pressure sensor or ebay 100 psi
    def autometer_2246(adc):
        volts = (adc / 4096.000) * 5.0
        return 25 * volts - 12.5

    # ebay 150 psi oil pressure sensor
    def ebay_150_psi(adc):
        volts = (adc / 4096.000) * 5.0
        return 37.5 * volts - 18.75

    def fuel_civic_eg_tank(adc):
        volts = (adc / 4096.000) * 4.80
        return int(-7.348540077 * pow(10, -1) * pow(volts, 2) - 32.27276861 * volts + 109.170896)
