<div style="text-align:center">
<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/hondash_kit.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/hondash_kit.png" height="300" />
</div>

## What's HonDash?

HonDash is an open source instrument cluster developed for Honda engines managed through [Hondata](https://www.hondata.com/) ECUs.

## Features

- [Data from K-Pro/S300 USB](https://hondash.com/VALUES.html)
- Minimal wiring involved
- [K-Pro v3/v4 and S300 v3 analog inputs available](https://hondash.com/SENSORS.html)
- Custom gauge color value depending
- [Display configuration through Wi-Fi](https://hondash.com/SETUP.html)
- [Fuel level through analog input](https://hondash.com/FUEL.html)
- [Data logger](https://hondash.com/DATALOGGER.html)
- [Keyboard as switch panel](https://hondash.com/KEYBOARD.html)
- Adjustable measurement units
- Day and night modes
- Odometer
- Running time

## Requirements (minimum)

- Hondata K-Pro v2* / v3 / v4 or Hondata S300 v3
- Raspberry Pi 3 Model B+ / Raspberry Pi 4 Model B
- HDMI/DSI/composite compatible screen

\* v2 only if it has on board data logging, check [here](https://www.hondata.com/kpro2)

```diff
- K-Pro must have the latest firmware from at least Kmanager V4.4.1
```

## Setup diagram

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/setup.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/setup.png" height="300" />

## Can I build my own?

Yes, the [software](https://hondash.com/SOFTWARE.html) is open source and the [hardware](https://hondash.com/HARDWARE.html) is commercial and easy to get.

## Known issues

- With K-Pro v2/v3 Hondata data logging (not the HonDash one) should be disabled to run HonDash
- In K-Pro map sensor would only show up to 1.8 bar
- Raspberry Pi 4 with old firmware could have WiFi connectivity problems while using the HDMI port, if this is happening to you please update the firmware <https://www.youtube.com/watch?v=FZ2Kfg8xnBw>

## Ready to run kit

Check [this](https://hondash.com/READYTORUN.html) out if you just want to buy everything assembled.
