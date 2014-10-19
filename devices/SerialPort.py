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
	    self.serialPort = Serial('/dev/ttyAMA0',38400,timeout=0.01)
            self.serialPort.open()
	    return 0
	    
