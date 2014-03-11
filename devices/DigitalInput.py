import RPi.GPIO as GPIO


class DigitalInput:
    def __init__(self, pin, callback):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.BOTH)
        #GPIO.add_event_callback(pin, callback)

    def value(self):
        if GPIO.input(self.pin) == 1:
            return False
        else:
            return True
