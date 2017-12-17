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

## Usage

Start ui:

```
python ui/ui.py
```

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

Connect a momentary switch to pins 5 and 6.

    curl https://pie.8bitjunkie.net/shutdown/setup-shutdown.sh | bash

cf. https://pie.8bitjunkie.net/retropie-shutdown-and-startup-switch-the-easy-way
