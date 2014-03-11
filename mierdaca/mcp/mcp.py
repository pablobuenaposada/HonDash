import spidev, time
spi = spidev.SpiDev()

spi.open(0,0)

def analog_read(channel):

    r = spi.xfer2([4 | 2 |(channel>>2), (channel &3) << 6,0])

    adc_out = ((r[1]&15) << 8) + r[2]

    return adc_out


while True:

    reading = analog_read(0)

    voltage = reading * 5.0 / 4096

    Temp = voltage * 99.5

    print("Reading=%d\tVoltage=%f\tTemp=%2.2f" % (reading, voltage,Temp))

    time.sleep(0.1)