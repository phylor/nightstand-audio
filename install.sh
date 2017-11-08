#!/bin/bash

CONFIG=/boot/config.txt
BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf

# Enable SPI
sudo sed $CONFIG -i -r -e "s/^#?((device_tree_param|dtparam)=([^,]*,)*spi)(=[^,]*)?/\1=on/"
sudo sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*spi[-_]bcm2708\)/#\1/"
#TODO: a reboot is required here: sudo reboot

# Install Kivy as per instructions of https://kivy.org/docs/installation/installation-rpi.html
sudo apt-get update
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
   pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python-dev libmtdev-dev \
   xclip
sudo pip install -U Cython==0.27.3
sudo pip install git+https://github.com/kivy/kivy.git@master

# Custom dependencies required by our own code
sudo apt-get install -y vlc

git clone https://github.com/lthiery/SPI-Py.git
PWD=$PWD/SPI-Py sudo python setup.py install

git clone https://github.com/mxgxw/MFRC522-python.git
