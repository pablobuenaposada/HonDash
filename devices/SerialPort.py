from serial import *


class SerialPort:
    def __init__(self):
        try:
            self.serialPort = Serial('/dev/ttyAMA0', 38400, timeout=0.01)
        except:
            pass

    def get_byte(self, address):
        try:
            self.serialPort.flushInput()
            self.serialPort.write(chr(address))
            response = self.serialPort.read(1)
            if len(response) <= 0:
                return 0
            else:
                return ord(response)
        except:
            try:
                if self.serialPort is None:
                    pass
                elif self.serialPort.isOpen:
                    self.serialPort.close()
                self.serialPort = Serial('/dev/ttyAMA0', 38400, timeout=0.01)
                return 0
            except:
                return 0

    def get_byte_from_three(self, address1, address2, address3):
        try:
            self.serialPort.flushInput()
            self.serialPort.write(chr(address1) + chr(address2) + chr(address3))
            response = self.serialPort.read(1)
            if len(response) <= 0:
                return 0
            else:
                return ord(response)
        except:
            try:
                if self.serialPort is None:
                    pass
                elif self.serialPort.isOpen:
                    self.serialPort.close()
                self.serialPort = Serial('/dev/ttyAMA0', 38400, timeout=0.01)
                return 0
            except:
                return 0
