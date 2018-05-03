from devices.digital_input import DigitalInput

di = DigitalInput(22)

while True:
    print(di.status())
