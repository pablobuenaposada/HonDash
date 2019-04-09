![alt tag](https://raw.github.com/pablobuenaposada/HonDash/master/docs/logo/hondash.png)

## How to run this project in a Raspberry Pi?
Get Raspbian (release date 2018-11-13) working in your raspberry, more info [here](https://www.raspberrypi.org/downloads/raspbian/)

Let's update:
```sh
sudo apt update
```

Install vim because reasons:
 ```sh
sudo apt install vim
```

Install this packages:
```sh
sudo apt install libatlas-base-dev libssl-dev libsnappy-dev
```

### SSH
Enable SSH through:
```sh
sudo raspi-config
```
Go to 5.Interfacing options --> enable both SSH

### Install the project
Clone this project:
```sh
cd /home/pi/Desktop/
git clone --recursive https://github.com/pablobuenaposada/HonDash.git
```

Being in the root of the project create de virtual enviroment:
```sh
cd HonDash/
make virtualenv_rpi

```
Later you can just run the project:
```sh
make run_rpi
```

### Hostname
Change the hostname from raspberrypi to hondash
```sh
sudo sed -i 's/raspberrypi/hondash/g' /etc/hostname
sudo sed -i 's/raspberrypi/hondash/g' /etc/hosts
```

### Enable hotspot
```sh
sudo apt install network-manager network-manager-gnome openvpn \openvpn-systemd-resolved network-manager-openvpn \network-manager-openvpn-gnome
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
sudo apt-get install nginx
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

### Disable screen saver
```sh
sudo apt-get install xscreensaver
```
Go to Preferences --> Screensaver --> disable screensaver.

### Disable SSH warning
```sh
sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh
```
### Boot faster
rcconf
disable bluethoot, alsa...


