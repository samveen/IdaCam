#!/usr/bin/env python
import six
import sys
import RPi.GPIO as GPIO
import time
import subprocess
import signal


btn_shutter=31
btn_up=35
btn_down=37

led_shutter=32
led_up=36
led_down=38

CAMERA=1
GALLERY=2

state=CAMERA
tty1_control= None
raspistill_control=None

def switch_to_camera():
    global state
    global tty1_control 
    global raspistill_control
    state=CAMERA
    GPIO.output(led_shutter,GPIO.HIGH)
    GPIO.output(led_up,     GPIO.LOW)
    GPIO.output(led_down,   GPIO.LOW)
    raspistill_control = subprocess.Popen(['raspistill', '-s', '-ts', '-o', 'DCIM/IMG_%d.jpg'])
    if tty1_control:
        tty1_control.stdin.write('q')

def switch_to_gallery():
    global state
    global tty1_control 
    global raspistill_control
    state=GALLERY
    GPIO.output(led_shutter,GPIO.LOW)
    GPIO.output(led_up,     GPIO.HIGH)
    GPIO.output(led_down,   GPIO.HIGH)
    tty1_control.stdin.write("\nfbi --readahead --cachemem 128 -a DCIM/*.jpg\nj")
    raspistill_control.terminate()


def on_button_press(channel):
    global state
    global tty1_control 
    global raspistill_control
    print("start state:{}".format(state))
    if channel==btn_shutter:
        if state == CAMERA:
            print "Click."
            raspistill_control.send_signal(signal.SIGUSR1)
        elif state == GALLERY:
            switch_to_camera()
    elif channel==btn_up:
        if state == GALLERY:
            tty1_control.stdin.write('k')
        elif state == CAMERA:
            switch_to_gallery()
    elif channel==btn_down:
        if state == GALLERY:
            tty1_control.stdin.write('j')
        elif state == CAMERA:
            switch_to_gallery()
    print("end state:{}".format(state))

try:

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(True)

    GPIO.setup(btn_shutter, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_up,      GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btn_down,    GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.setup(led_shutter, GPIO.OUT)
    GPIO.setup(led_up,      GPIO.OUT)
    GPIO.setup(led_down,    GPIO.OUT)

    switch_to_camera()

    GPIO.add_event_detect(btn_shutter, GPIO.FALLING,callback=on_button_press,bouncetime=300)
    GPIO.add_event_detect(btn_up,      GPIO.FALLING,callback=on_button_press,bouncetime=300)
    GPIO.add_event_detect(btn_down,    GPIO.FALLING,callback=on_button_press,bouncetime=300)

    tty1_control = subprocess.Popen(["fauxcon", "-C", "tty1"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        time.sleep(1)
except:
    # Clean up
    GPIO.cleanup()
    if raspistill_control:
        raspistill_control.terminate()
    if tty1_control:
        tty1_control.stdin.write('q')
    print("Unexpected error: {}".format(sys.exc_info()[0]))
    raise

GPIO.cleanup()
