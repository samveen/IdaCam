#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

led_shutter=32
led_up=36

pin=36

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)
print "start" 
for i in range(5):
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(1)
print "done" 
