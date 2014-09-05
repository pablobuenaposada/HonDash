from serial import *

class SerialPort:

    def __init__(self):
        self.serialPort = Serial('/dev/ttyAMA0',38400,timeout=0.01)
        self.serialPort.open()

    def getByte(self,address):
        self.serialPort.flushInput()
        self.serialPort.write(chr(address))
        response = self.serialPort.read(1)
        if len(response) <= 0 : return 1
        else: return ord(response)
    
