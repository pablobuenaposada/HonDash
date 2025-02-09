# Configure my setup

HonDash offers a Wi-Fi network all the time where you can set your preferences, get your laptop/tablet/phone and connect to it, no password required.

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/wifi.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/wifi.png" height="500"/>

Once your are connected to it, simply open your browser and type:

* [hondash.local/](http://hondash.local/) ([10.42.0.1/](http://10.42.0.1/) from `Android` devices) to see the actual dashboard
* [hondash.local/setup/](http://hondash.local/setup/) ([10.42.0.1/setup](http://10.42.0.1/setup/) from `Android` devices) to configure the dashboard

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/wifi_setup.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/wifi_setup.png" height="500"/>

After saving the changes you should see new setup already applied.

## O2 with target

O2 sensor configuration allows to use the target lambda/AFR against the actual lambda/AFR for "sectors" color part.
To use this feature you need to set target option to true and then use "sectors" accordingly like in the following example:

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/target.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/target.png" height="500"/>

In this example, the AFR graph will be shown in red if the difference between the target and actual AFR exceeds 0.4, whether positive or negative. Otherwise, it will remain uncolored.

Of course this would not work without this option activated from K-manager:

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/kmanager_target.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/kmanager_target.png" height="500"/>

## Gearbox ratio

If your speedometer or gear indicator are not accurate it's most likely caused by wrong gear ratios configuration in K-Pro.

To solve this, check out this section under `Gear comp` tab:

<img src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/gearbox.png" data-canonical-src="https://raw.github.com/pablobuenaposada/HonDash/master/docs/readme/gearbox.png" height="600"/>

In <span style="color:red">*red* </span>you can see the current ratios by gear you can modify them manually or just select one of the predefined gearbox ratios from the button marked in <span style="color:green">*green*</span>.

For more information about K-series gearbox ratios [check this](https://raw.github.com/pablobuenaposada/HonDash/master/docs/images/ratios.jpg).
