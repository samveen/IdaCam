#/usr/bin/env python
#importing the necessary modules
import sys
from datetime import datetime
from gpiozero import Button
import picamera
import time

# Waveshare LCD's keys
k1=Button(18) # GPIO18, phys pin 12, key 1
k2=Button(23) # GPIO23, phys pin 16, key 2
k3=Button(24) # GPIO24, phys pin 18, key 3

cam=picamera.PiCamera()
running = True

#use this to set the resolution if you dislike the default values
#pc.resolution = (1024, 768)


def picture():
        timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
	cam.capture('IMG_'+str(timestamp)+'.jpg') #taking the picture

def main():
    cam.start_preview() #running the preview
    b.when_pressed=picture
    try:
        while running:
            print('Active')#displaying 'active' to the shell
            time.sleep(1)
    #we detect Ctrl-C then quit the program
    except KeyboardInterrupt:
        cam.stop_preview()
        running = False

if __name__ == '__main__':
    print("Starting up Camera app")
        sys.exit(main())

# vim: ts=4 sw=4 expandtab:
