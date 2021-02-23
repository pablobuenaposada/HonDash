# Fuel level 

In order to display the fuel level you must hook the fuel level sender of your car to one of the analog inputs of the K-Pro.

Later on you will be able to read this analog input from the K-Pro and translate it to something human readable in HonDash. 

This is necessary because from factory fuel level signal is not sent to the ECU, the signal is just sent directly to the stock car cluster.

## Wiring
<br/>
<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/fuel.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/fuel.png" height="400"/>

Fuel tank | Resistor value | Cabin harness wire color | Specs | Voltage (V) at 0% | Voltage (V) at 100%
------- | -------------- | ------------- | ------------- | ------------- | -------------
Civic EG | 56Ω 1 watt | yellow/white | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/civic_eg.jpg) | 3,31 | 0,17
Civic EK | 56Ω 1 watt | yellow/black | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/civic_ek.png) | 3,29 | 0,29
S2000 | 56Ω 1 watt | yellow/black | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/s2000.png) | 3,5 | 0,9
Integra DC5 | 56Ω 1 watt | | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/dc5.png) | 3,51 | 0,82
Accord CL9 | 56Ω 1 watt | | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/cl9.jpeg) | 4,66 | 1,25
MR2 W20 | 56Ω 1 watt | N/A | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/mr2_w20.png) | 3,31 | 0,24
MR2 W30 | 56Ω 1 watt | N/A | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/mr2_w30.png) | 3,87 | 1,1
MX5 NA | 56Ω 1 watt | N/A | [Available](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/fuel_gauges/mx5_na.png) | 3,14 | 0,55

<br/>
 
E5 pin is usually empty in the engine harness, to get a wire in there you need an old pigtail from other harness or you can buy them new on-line fairly cheap, the manufacturer is `TE Connectivity` and the reference is `316836-1`.

Check E5 location [here](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/prb.jpeg)

## K-manager setup
Even though this step is not necessary for HonDash, is always good to setup the fuel level in K-manager too, just for troubleshoot problems in this part it's already worth it.

Go to `Parameters` -> `Analog Inputs` and fill the chosen analog port like this:

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/kpro_fuel.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/kpro_fuel.png" height="600"/>

<br/>
The values within the red square (Civic EG example) should be filled according the previous table (<u>use comma as decimal separator</u>).

Note that the order of the rows is important, first row should contain the 100% and second one 0%, check the previous picture in detail.

After reuploading the calibration, you should be able to see your current fuel level in the display window after adding this new parameter.

## HonDash setup
Open your [configuration](/SETUP.html)

Go to your desired analog channel and select `custom` as formula and fill min and max voltage as described in the previous table (<u>use dot as decimal separator</u>) and min value as 0 and max value as 100.

Here is an example for Civic EG:

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/fuel_analog.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/fuel_analog.png"/>

## ⚠ Warning
K-Pro inputs are rate up to 5v max, double check this installation otherwise you will end damaging the K-Pro board and possibly the entire ECU.

A common practice for stock clusters in cars is to supply the fuel level unit with 12v from the actual cluster, so in order to run the fuel level in HonDash you will need to be completely sure that non other device is supplying power to the fuel level sender, check you car schematics, **disconnect the fuel level sender from your original cluster plugs** and use a multimeter to verify that the signal sent to K-Pro does not exceed 5v at all.

## Your fuel tank not in the list?
Get your fuel level sender specs (resistance when empty & full) and calculate the voltage that the hondata should recieve:
<br/>
<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/voltage_divider.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/voltage_divider.png"/>
<br/>
and use the next formula for calculate the voltage:
<br/>
<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/tank_formula.svg" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/tank_formula.svg"/>
<br/>
for example, for a Civic EG with an empty tank:
<br/>
<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/tank_formula_civic_eg.svg" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/tank_formula_civic_eg.svg"/>
<br/>
