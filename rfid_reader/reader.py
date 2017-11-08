#!/usr/bin/env python

import sys
import os

# Set import path to MFRC522 library
sys.path.append(os.path.abspath("./MFRC522-python"))

if sys.platform.startswith('linux'):
    import RPi.GPIO as GPIO
    import MFRC522
    import signal

sys.path.append(os.path.abspath("common"))
from message_queue import MessageQueue

class RfidReader():

    def __init__(self):
        self.loops_until_empty = 20

        # Hook the SIGINT
        #signal.signal(signal.SIGINT, end_read)
        
        self.MIFAREReader = MFRC522.MFRC522()
        
        self.last_uid = ''
        self.loops = 0
        
    # Capture SIGINT for cleanup when the script is aborted
    def end_read(self, signal, frame):
        print "Ctrl+C captured, cleaning up.."
        GPIO.cleanup()
        sys.exit(0)
    
    def read_rfid(self, callback):
        # Scan for cards    
        (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        
        # If no card is found
        if status != self.MIFAREReader.MI_OK and self.loops > self.loops_until_empty:
            if len(self.last_uid) > 0:
                callback(self.last_uid, "figurine_removed")
    
            self.last_uid = ''
            return
        
        # Get the UID of the card
        (status,uid) = self.MIFAREReader.MFRC522_Anticoll()
        
        # If we have the UID, continue
        if status == self.MIFAREReader.MI_OK:
            self.loops = 0
            uid_str = '.'.join(str(x) for x in uid)
        
            if self.last_uid != uid_str:
                self.last_uid = uid_str
                callback(uid_str, "figurine_added")
