import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from devices.MCP3208 import MCP3208

an = MCP3208()


def adc2oiltemp(adc):
    volts = (adc/4096.000)*4.80
    return (int)(-9.805174198*pow(10,-1)*pow(volts,9)+23.4368155*pow(volts,8)-240.7430517*pow(volts,7)+1390.11628*pow(volts,6)-4955.008229*pow(volts,5)+11266.31187*pow(volts,4)-16289.93484*pow(volts,3)+14423.41426*pow(volts,2)-7152.975474*volts+1697.497838)


while True:
    print(an.adc_with_formula(0,adc2oiltemp))