#!/bin/sh

curl -sSL https://get.docker.com | sh
sudo usermod -aG docker ${USER}
sudo systemctl enable docker
sudo apt update
sudo apt install python3 python3-pip vim unclutter
curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

cd /home/pi/Desktop/
git clone https://github.com/pablobuenaposada/HonDash.git
cd HonDash
export PYTHON_KEYRING_BACKEND=keyring.backends.fail.Keyring
make venv

cd /home/pi/Desktop/
git clone https://github.com/pablobuenaposada/HonDash-frontend.git
cd HonDash-frontend
make docker/build

crontab /home/pi/Desktop/HonDash/crontab/crontab

echo '@unclutter -idle 0.1' | sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null
env DISPLAY=:0.0 pcmanfm -w /home/pi/Desktop/HonDash/docs/wallpaper/wallpaper.png --wallpaper-mode=stretch
sudo rm /etc/xdg/lxsession/LXDE-pi/sshpwd.sh
{ echo '@xset s off'; echo '@xset -dpms'; echo '@xset s noblank'; } | sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null
