import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.digital_input import DigitalInput

di = DigitalInput(22)

while True:
    print(di.status())
