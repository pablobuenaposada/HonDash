import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(27, GPIO.BOTH,bouncetime=100)
def my_callback(pin):
    print "aaaaa"
GPIO.add_event_callback(27,callback=my_callback)

while True:
    None
