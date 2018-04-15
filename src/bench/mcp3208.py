import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.MCP3208 import MCP3208

an = MCP3208()

while True:
    print(an.adc(7))