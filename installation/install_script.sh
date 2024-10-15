#!/bin/sh

curl -sSL https://get.docker.com | sh
sudo usermod -aG docker ${USER}
sudo systemctl enable docker
sudo apt update
sudo apt install -y python3 python3-pip vim unclutter xdotool
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
sudo su
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

cd /home/pi/Desktop/
git clone https://github.com/pablobuenaposada/HonDash.git
cd HonDash
git checkout refresh
make venv
docker compose up -d nginx
touch /home/pi/Desktop/HonDash/hondash.log
sudo chmod 777 /home/pi/Desktop/HonDash/hondash.log

cd /home/pi/Desktop/
git clone https://github.com/pablobuenaposada/HonDash-frontend.git
cd HonDash-frontend
make docker/build
docker run -d --restart=unless-stopped --network=hondash_main_network -p 80:80 hondash-frontend

cp /home/pi/Desktop/HonDash/installation/services/chromium.service /etc/systemd/system/
cp /home/pi/Desktop/HonDash/installation/services/chromium-refresh.service /etc/systemd/system/
cp /home/pi/Desktop/HonDash/installation/services/hondash.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable chromium.service
sudo systemctl start chromium.service
sudo systemctl enable chromium-refresh.service
sudo systemctl start chromium-refresh.service
sudo systemctl enable hondash.service
sudo systemctl start hondash.service

echo '@unclutter -idle 0.1' | sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null
env DISPLAY=:0.0 pcmanfm -w /home/pi/Desktop/HonDash/docs/wallpaper/wallpaper.png --wallpaper-mode=stretch
sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh
{ echo '@xset s off'; echo '@xset -dpms'; echo '@xset s noblank'; } | sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null
echo 'dtparam=i2c_vc_baudrate=50000' | sudo tee -a /boot/firmware/config.txt > /dev/null

sudo systemctl disable bluetooth.service
sudo systemctl disable hciuart.service
sudo systemctl disable cron.service
sudo systemctl disable cups-browsed.service
sudo systemctl disable triggerhappy.service