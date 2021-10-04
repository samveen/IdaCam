#!/usr/bin/env python
import subprocess
import glob
import time

#try:
fl=glob.glob("DCIM/*.jpg")
p = subprocess.Popen(["fbi", "-v", "-v"]+fl,std )
while True:
    sleep(10)

#except:
# Clean up
#    print "except."
