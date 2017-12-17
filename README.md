# Nightstand Audio

## Installation

It is advised to use Raspbian Lite (without graphical interface). The UI in this project runs fine without Xorg or similar.

You need to be connected to the Internet for the installation. Either connect a network cable, or connect to Wifi.

```shell
sudo apt-get install -y git
git clone https://github.com/phylor/nightstand-audio
cd nightstand-audio
./install.sh
```

If your screen is upside-down, add `lcd_rotate=2` to `/boot/config.txt`. It rotates the display as well as the touch coordinates by 180 degrees.

## Prepare a USB drive

Music is stored on a USB drive. The USB drive must have the following directory structure:

```
.
├── audio/
└── figurines/
```

Store all audio files in the `audio` directory. Leave the `figurines` directory empty. It is used to match figurines and audio files.

To automount the USB drive, add the following line to your `/etc/fstab`:

```
/dev/sda1 /mnt vfat rw,uid=1000,gid=1000 0 0
```

## Usage

Start ui:

```
python ui/ui.py
```

To automatically start the application when starting the Raspberry Pi, activate `autologin to console` in `Boot Options` when running `sudo raspi-config`. Then add the following to the end of `.bashrc` of the `pi` user:

```
if [ $(tty) == '/dev/tty1' ]; then
  cd nightstand-audio
  python ui/ui.py
fi

## Troubleshooting

To test the RFID reader:

```
./rfid_reader/reader.py
```

If a device has been read, it prints its UID.

Simulate a figurine placed onto the box:

```
```

## Start/Shutdown button

Connect a momentary switch to pins 5 and 25. Note that when using the official Raspberry Pi Touchscreen pin 5 is already used. You can hook the button as well as the touchscreen both to pin 5 though (e.g. use a jumper bridge).

    curl https://pie.8bitjunkie.net/shutdown/setup-shutdown.sh | bash

cf. https://pie.8bitjunkie.net/retropie-shutdown-and-startup-switch-the-easy-way
