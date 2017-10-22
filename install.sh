#!/bin/bash

CONFIG=/boot/config.txt
BLACKLIST=/etc/modprobe.d/raspi-blacklist.conf

# Enable SPI
sudo sed $CONFIG -i -r -e "s/^#?((device_tree_param|dtparam)=([^,]*,)*spi)(=[^,]*)?/\1=on/"
sudo sed $BLACKLIST -i -e "s/^\(blacklist[[:space:]]*spi[-_]bcm2708\)/#\1/"
#TODO: a reboot is required here: sudo reboot


# Install python libraries
sudo apt-get update
sudo apt-get install -y git python-dev
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo python setup.py install
cd ..

# brew install gst-plugins-bad gst-plugins-good
sudo apt-get install -y python-kivy rabbitmq-server vlc
sudo pip install pika

git clone https://github.com/mxgxw/MFRC522-python.git
