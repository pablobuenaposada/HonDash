from serial import *

class SerialPort:

    def __init__(self):
        self.serialPort = Serial('/dev/ttyAMA0',38400,timeout=1)
        self.serialPort.open()

    def getByte(address):
        self.serialPort.write(chr(address))
        return serialPort.read(1)
        
