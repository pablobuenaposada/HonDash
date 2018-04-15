from devices.digital_input import DigitalInput

while True:
    di = DigitalInput(22, None)
    print(di.value())
