![alt tag](https://raw.github.com/pablobuenaposada/HonDash/master/docs/logo/hondash.png)

## How to run this project in a Raspberry Pi?
Get Raspbian (release date 2020-02-13) working in your raspberry, more info [here](https://www.raspberrypi.org/downloads/raspbian/)

### SSH
Enable SSH through:
```sh
sudo raspi-config
```
Go to 5.Interfacing options --> enable both SSH

ssh into it:
```sh
ssh pi@raspberrypi.local
```

Let's update:
```sh
sudo apt update
```

Install vim because reasons:
 ```sh
sudo apt -y install vim
```

### Install the project
Clone this project:
```sh
cd /home/pi/Desktop/
git clone https://github.com/pablobuenaposada/HonDash.git
cd HonDash/
```

Install dependencies:
```sh
sudo make system_dependencies
```

Create de virtual enviroment:
```sh
make virtualenv
```
Later you can just run the project:
```sh
make run_rpi
```

### Hostname
Change the hostname from raspberrypi to hondash
```sh
sudo sed -i 's/raspberrypi/hondash/g' /etc/hostname /etc/hosts
```

### Enable hotspot
```sh
sudo apt install network-manager network-manager-gnome openvpn \
openvpn-systemd-resolved network-manager-openvpn \
network-manager-openvpn-gnome
```

```sh
sudo apt purge openresolv dhcpcd5
```
reboot and run this: 

```sh
sudo ln -sf /lib/systemd/resolv.conf /etc/resolv.conf
```

Right click on the desktop bar and remove 'Wireless & Wired Network'

Reboot

Right click on the network manager and add a WiFi connection type, connection name: HonDash, ssid: HonDash, mode: Hotspot

### Nginx for enable the setup tool
```sh
sudo apt -y install nginx
```

```sh
sudo cp /home/pi/Desktop/HonDash/config/nginx/default /etc/nginx/sites-enabled/default
```

```sh
sudo /etc/init.d/nginx start
```

## Optional tricks
### HonDash at startup
```sh
crontab /home/pi/Desktop/HonDash/config/cron/cron
```

### Remove wizard setup message
```sh
sudo rm /etc/xdg/autostart/piwiz.desktop
```

### Hide mouse pointer
```sh
sudo apt install unclutter
sudo vim /etc/xdg/lxsession/LXDE-pi/autostart
```
add this line:
```sh
@unclutter -idle 0.1
```

### Wallpaper
```sh
env DISPLAY=:0.0 pcmanfm -w /home/pi/Desktop/HonDash/docs/wallpaper/wallpaper.png --wallpaper-mode=stretch
```

### Disable screen saver
```sh
sudo apt -y install xscreensaver
```
Go to Preferences --> Screensaver --> disable screensaver.

### Disable SSH warning
```sh
sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh
```
### Boot faster
rcconf
disable bluethoot, alsa...

### Create SD card image file
Check your sd card path with:
```sh
diskutil list
```

use the provided make command to build a full sd card image:
```sh
make sd-image/create path=/dev/rdisk6
```

shrink it:
```sh
make sd-image/shrink
```
