from serial import *

class SerialPort:

    def __init__(self):
        try:
            self.serialPort = Serial('/dev/ttyAMA0',38400,timeout=0.01)
            self.serialPort.open()
        except:
            pass

    def getByte(self,address):
        try:
            self.serialPort.flushInput()
            self.serialPort.write(chr(address))
            response = self.serialPort.read(1)
            if len(response) <= 0 : return 1
            else: return ord(response)
        except:
            try:
                self.serialPort.close()
                self.serialPort = Serial('/dev/ttyAMA0',38400,timeout=0.01)
                self.serialPort.open()
                return 1
            except: return 1

    def getByteFromThree(self,address1,address2,address3):
        try:
            self.serialPort.flushInput()
            self.serialPort.write(chr(address1))
            self.serialPort.write(chr(address2))
            self.serialPort.write(chr(address3))
            response = self.serialPort.read(1)
            if len(response) <= 0 : return 1
            else: return ord(response)
        except:
            try:
                self.serialPort.close()
                self.serialPort = Serial('/dev/ttyAMA0',38400,timeout=0.01)
                self.serialPort.open()
                return 1
            except: return 1
