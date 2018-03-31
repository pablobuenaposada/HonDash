class Formula:
    def __init__(self):
        pass

    # conversion for VDO 323-057 sensor powered by 4.8v and read with a 56ohms voltage divider
    def vdo_323_057(self, adc):
        volts = (adc / 4096.000) * 4.80
        return (int)(-9.805174198 * pow(10, -1) * pow(volts, 9) + 23.4368155 * pow(volts, 8) - 240.7430517 * pow(volts,
                                                                                                                 7) + 1390.11628 * pow(
            volts, 6) - 4955.008229 * pow(volts, 5) + 11266.31187 * pow(volts, 4) - 16289.93484 * pow(volts,
                                                                                                      3) + 14423.41426 * pow(
            volts, 2) - 7152.975474 * volts + 1697.497838)

    # conversion for VDO 360-004 sensor powered by 4.8v and read with a 56ohms voltage divider
    def vdo_360_004(self, adc):
        volts = (adc/4096.000)*4.80
        return round(7.671035919*pow(10,-2)*pow(volts,7)-1.077184901*pow(volts,6)+6.295494139*pow(volts,5)-19.62567902*pow(volts,4)+35.08161116*pow(volts,3)-35.51613665*pow(volts,2)+19.52857924*volts-4.551671147,1)

    def fuel_civic_eg_tank(self, adc):
        volts = (adc / 4096.000) * 4.80
        return int(-7.348540077 * pow(10, -1) * pow(volts, 2) - 32.27276861 * volts + 109.170896)