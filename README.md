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
- Battery voltage
- A/F ratio
- Throttle position
- Speed
- RPM
- VTC cam angle
- Coolant temperature
- Intake air temperature
- Gear
- Electronic power steering pressure
- Service connector
- Reverse lock
- Brake switch
- A/C switch
- A/C clutch
- Fuel relay
- Manifold absolute pressure
- Malfunction indicator light
- Ecu type
- Ignition degree
- K-Pro serial number
- K-Pro firmware version
- Analog inputs

## Optional HonDash board

This board offers:
8 Digital inputs
8 Analog inputs (4 resistor based + 4 voltage based)

## Standalone installation

Once you are inside the HonDash project folder run this:
```sh
export PYTHONPATH='.'
```
