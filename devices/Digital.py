import RPi.GPIO as GPIO

class Digital:

    def __init__(self):
	None

    def setInput(self,pin):
	GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)    

    def getValue(self,pin):
	value = GPIO.input(pin)
	if value == 1: return True
	else: return False	

    def addEvent(self,pin,callback):
	GPIO.add_event_detect(pin,GPIO.BOTH,bouncetime=10)
	GPIO.add_event_callback(pin,callback)
