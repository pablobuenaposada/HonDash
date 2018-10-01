![alt tag](https://raw.github.com/pablobuenaposada/HonDash/master/docs/logo/hondash.png)

## Fuel level 

In order to display the fuel level you must hook the fuel level sender of your car to one of the analog inputs of the K-Pro.

Later on you will be able to read this analog input from the K-Pro and translate it to something human readable in HonDash. 

Here is a schematic diagram:

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/fuel.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/fuel.png" height="300" />

Fuel tank | Resistor value
------- | -----
Civic EG | 56Ω 1/4 watt
S2000 | 56Ω 1/4 watt

> ⚠️ WARNING: K-Pro inputs are rate up to 5v max, double check this installation otherwise you will end damaging the K-Pro board and possibly the entire ECU.

> A common practice for stock clusters in cars is to supply the fuel level unit with 12v from the actual cluster, so in order to run the fuel level in HonDash you will need to be completely sure that non other device is supplying power to the fuel level sender, check you car schematics, **disconnect the fuel level sender from your original cluster plugs** and use a multimeter to verify that the signal sent to K-Pro does not exceed 5v at all.
