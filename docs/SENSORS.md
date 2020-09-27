# Optional sensors

Optional analog sensors are also read from K-Pro and displayed in HonDash, you can read how to wire them in the official Hondata guide:
* [Analog wideband](https://www.hondata.com/help/kmanager/index.html?analog_wideband.htm)
* [Analog pressure](https://www.hondata.com/help/kmanager/index.html?analog_pressure.htm)
* [Analog temperature](https://www.hondata.com/help/kmanager/index.html?analog_temperature.htm)

Some digital ones also work with HonDash:
* [Digital ethanol content](https://www.hondata.com/help/kmanager/index.html?flex_fuel.htm)

Once the sensor is wired and correctly working in K-manager you can setup HonDash to display it, check the [setup](https://pablobuenaposada.github.io/HonDash/SETUP.html) guide for that.

For now not all the sensors that work with Hondata can be read in HonDash but they would be added in the future, here is the list:

Sensor type | Reference | Thread | Working range
------- | --------- | ------ | ------
Wideband | All K-Pro supported ones | - | -
Ethanol content | [All K-Pro supported ones](https://www.hondata.com/help/kmanager/index.html?flex_fuel.htm) | - | -
Pressure | Autometer 2246 / eBay 100 psi | 1/8 NPT | 0 - 100 psi / 0.5V - 4.5V
Pressure | eBay 150 psi | 1/8 NPT | 0 - 150 psi / 0.5V - 4.5V
Temperature | VDO 323-057 (inline with 56Ω resistor) | 1/8 NPT | -40 - 150 ºC
Temperature | AEM 30-2012 / Delphi 12160855 | 1/8 NPT | -40 - 150 ºC     
Temperature | Bosch 0280130039 / 0280130026 | M12x1.5mm | -40 - 130-140 ºC