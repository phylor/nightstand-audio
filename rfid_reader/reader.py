#!/usr/bin/env python

import sys
import os

# Set import path to MFRC522 library
sys.path.append(os.path.abspath("./MFRC522-python"))

import RPi.GPIO as GPIO
import MFRC522
import signal

def send_event(uid, event):
    content = { "uid": uid, "event": event }
    
    queue = MessageQueue()
    queue.send(content)

def read_rfid():
    continue_reading = True
    
    # Capture SIGINT for cleanup when the script is aborted
    def end_read(signal,frame):
        global continue_reading
        print "Ctrl+C captured, ending read."
        continue_reading = False
        GPIO.cleanup()
    
    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)
    
    MIFAREReader = MFRC522.MFRC522()
    
    last_uid = ''
    loops_until_empty = 20
    loops = 0
    
    while continue_reading:
        loops += 1
        
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
        # If no card is found
        if status != MIFAREReader.MI_OK and loops > loops_until_empty:
            last_uid = ''
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:
            loops = 0
    	uid_str = '.'.join(str(x) for x in uid)
    
    	if last_uid == uid_str:
                continue
    
    	last_uid = uid_str
    	print last_uid
    
        send_event(uid_str, "figurine_added")

if len(sys.argv) > 1:
    send_event("12.90.49.232.97", sys.argv[1])
else:
    read_rfid()
