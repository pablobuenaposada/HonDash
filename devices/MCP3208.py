import spidev

class MCP3208:

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)

    def getADC(self,channel):
        raw = self.spi.xfer2([4 | 2 |(channel>>2), (channel &3) << 6,0])
        adc_out = ((raw[1]&15) << 8) + raw[2]
        return adc_out

    def getVoltage(self,channel):
        adc = getADC(channel)
        return adc * 5.0 / 4096
