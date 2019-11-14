## What's HonDash?

HonDash is an open source instrument cluster developed for Honda engines managed through [Hondata](https://www.hondata.com/) ECUs.

## Features
- Pulls data from K-Pro USB
- Minimal wiring involved
- [K-Pro v3/v4 analog inputs available](http://hondash.com/SENSORS.html)
- Custom gauge color value depending
- [Display configuration through Wi-Fi](http://hondash.com/SETUP.html)
- [Fuel level through K-Pro analog input](http://hondash.com/FUEL.html)
- Adjustable measurement units
- Odometer
- Running time

## Requirements (minimum)

- Hondata K-Pro* ECU v2 / v3 / v4
- Raspberry Pi 3 Model B+
- HDMI screen

\* v2 only if it has on board datalogging, check [here](https://www.hondata.com/kpro2)

\* K-Pro should have the latest firmware from Kmanager V4.4.1 

## Setup diagram

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/setup.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/setup.png" height="300" />

## Specifications

List of values available through K-Pro right now:

Acronym | Value | K-Pro v2 | K-Pro v3 | K-Pro v4
------- | ----- | :------: | :------: | :------:
BAT | Battery voltage |:white_check_mark:|:white_check_mark:|:white_check_mark:
AFR | A/F ratio |  |:white_check_mark:|:white_check_mark:
TPS | Throttle position |:white_check_mark:|:white_check_mark:|:white_check_mark:
VSS | Speed |  |:white_check_mark:|:white_check_mark:
RPM | Revs. per minute |  |:white_check_mark:|:white_check_mark:
CAM | VTC cam angle |  |:white_check_mark:|:white_check_mark:
CLV | Calculated load value |  |  |
ECT | Coolant temperature |:white_check_mark:|:white_check_mark:|:white_check_mark:
ETH | Ethanol content |  |  |:white_check_mark:
FLT | Fuel temperature |  |  |:white_check_mark:
IAT | Intake air temperature |:white_check_mark:|:white_check_mark:|:white_check_mark:
GEAR | Gear |  |:white_check_mark:|:white_check_mark:
EPS | Electronic power steering pressure |:white_check_mark:|  |:white_check_mark:
SCS | Service connector |:white_check_mark:|  |:white_check_mark:
RVSLCK | Reverse lock |  |  |:white_check_mark:
BKSW | Brake switch |  |  |:white_check_mark:
ACSW | A/C switch |  |  |:white_check_mark:
ACCL | A/C clutch |  |  |:white_check_mark:
FLR | Fuel relay |  |  |:white_check_mark:
FANC | Fan control |:white_check_mark:|:white_check_mark:|:white_check_mark:
MAP | Manifold absolute pressure |:white_check_mark:|:white_check_mark:|:white_check_mark:
MIL | Malfunction indicator light |  |  |:white_check_mark:
ECU | Ecu type |  |  |:white_check_mark:
IGN | Ignition status |  |  |:white_check_mark:
SRL | K-Pro serial number |  |  |:white_check_mark:
FIRM | K-Pro firmware version |  |  |:white_check_mark:
AN | Analog inputs | :x: |:white_check_mark:|:white_check_mark:
 