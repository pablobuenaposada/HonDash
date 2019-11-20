## What's HonDash?

HonDash is an open source instrument cluster developed for Honda engines managed through [Hondata](https://www.hondata.com/) ECUs.

## Features
- Pulls data from the K-Pro USB
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

```diff
- K-Pro must have the latest firmware from Kmanager V4.4.1
```


## Setup diagram

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/setup.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/setup.png" height="300" />
