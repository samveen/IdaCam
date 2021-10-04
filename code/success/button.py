#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
shutter=31
up=35
down=37
key1=12
key2=16
key3=18
channel=down

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)

GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    if GPIO.input(channel):
        print('Input was HIGH')
    else:
        print('Input was LOW')
    time.sleep(1)

GPIO.cleanup() # Clean up
