# Data logger

HonDash offers an alternative data logger rather than the onboard that Hondata provides.

Log files are around 30 minutes max (around 3MB), if your data logging session overpass this time the log will be split into multiple files.

For reference, using a 16GB you can store up to 2000 hours of logs. 

## Activation

You can configure its activation through HonDash [configuration](/SETUP.html) page.

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/setup.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/setup.png"/>

`autostart`: if set to true datalogging will start as soon as the dashboard is loaded.

You can always start/stop a datalogging session pressing key `0` through [USB keyboard](/KEYBOARD.html).

The status is shown in the dashboard through this icon:

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/status.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/status.png"/>

## Log retrieval

In order to download the log you need to connect to:
* [hondash.local/datalogs/](http://hondash.local/datalogs/) ([10.42.0.1/datalogs](http://10.42.0.1/datalogs/) from `Android` devices)

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/datalogs.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/datalogs.png"/>

You can download specific session in `.csv` format by clicking on it or also remove it through ❌ button, if you try to log when there´s no more free space, older logs will be removed.

## Open log
You can use any log viewer compatible with csv files, we recommend [DATAZAP](https://datazap.me/) because it's free and easy to use, just create an account and upload HonDash log files.

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/datazap.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/datalogger/datazap.png"/>
