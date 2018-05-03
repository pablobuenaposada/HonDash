![alt tag](https://raw.github.com/pablobuenaposada/HonDash/kpro/docs/logo/hondash.png)

[![alt tag](https://codecov.io/gh/pablobuenaposada/hondash/branch/kpro/graph/badge.svg)](https://codecov.io/gh/pablobuenaposada/hondash/)

## What's HonDash?

HonDash is an open source instrument cluster developed for Honda engines.

## Requirements (minimum)

- Hondata K-Pro ECU v2* / v3 / v4
- Raspberry Pi 3 Model B/B+
- HDMI screen

\* v2 only if it has on board datalogging, check [here](https://www.hondata.com/kpro2)

## Setup diagram

<img src="https://raw.github.com/pablobuenaposada/HonDash/kpro/docs/readme/setup.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/kpro/docs/readme/setup.png" height="300" />

## Specifications

List of values available through K-Pro right now:

Acronym | Value | K-Pro v2 | K-Pro v3 | K-Pro v4
------- | ----- | :------: | :------: | :------:
BAT | Battery voltage |  |  |:white_check_mark:
AFR | A/F ratio |  |  |:white_check_mark:
TPS | Throttle position |  |  |:white_check_mark:
VSS | Speed |  |  |:white_check_mark:
RPM | Revs. per minute |  |  |:white_check_mark:
VTC | VTC cam angle |  |  |:white_check_mark:
CLV | Calculated load value |  |  |
ECT | Coolant temperature |  |  |:white_check_mark:
ETH | Ethanol content |  |  |
FT | Fuel temperature |  |  |
IAT | Intake air temperature |  |  |:white_check_mark:
GEAR | Gear |  |  |:white_check_mark:
EPS | Electronic power steering pressure |  |  |:white_check_mark:
SCS | Service connector |  |  |:white_check_mark:
RVSLCK | Reverse lock |  |  |:white_check_mark:
BKSW | Brake switch |  |  |:white_check_mark:
ACSW | A/C switch |  |  |:white_check_mark:
ACCL | A/C clutch |  |  |:white_check_mark:
FLR | Fuel relay |  |  |:white_check_mark:
MAP | Manifold absolute pressure |  |  |:white_check_mark:
MIL | Malfunction indicator light |  |  |:white_check_mark:
ECU | Ecu type |  |  |:white_check_mark:
IGN | Ignition advance |  |  |:white_check_mark:
SRL | K-Pro serial number |  |  |:white_check_mark:
FIRM | K-Pro firmware version |  |  |:white_check_mark:
AN | Analog inputs | :x: |  |:white_check_mark:

## Optional HonDash board

This board is attached on top of the Raspberry and offers the ability to connect inputs that K-Pro can not manage or for safety reasons it's better to wire them to this board and not risk the K-Pro in case something goes wrong.

In detail the board offers:
* 8x 12v digital inputs (perfect for turn signal indicators, high beam indicator, oil pressure warning, etc...)
* 8x 5v analog inputs (4 resistor based + 4 voltage based)

## Standalone installation

Once you are inside the HonDash project folder run this:
```sh
export PYTHONPATH='src'
```
