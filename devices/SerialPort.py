from serial import *

class SerialPort:

    def __init__(self):
        self.serialPort = Serial('/dev/ttyAMA0',38400,timeout=0)
        self.serialPort.open()

    def getByte(self,address):
        self.serialPort.write(chr(address))
        response = self.serialPort.read(1)
        if type(response) is int:
            return response
        else:
            return 1
