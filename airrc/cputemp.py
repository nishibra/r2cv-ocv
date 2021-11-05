#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
#
import subprocess
import time
from time import sleep
cmd="cat /sys/class/thermal/thermal_zone0/temp"
while(1):
    aa=subprocess.check_output(cmd.split())
    print ("CPU temp.=",(int(aa))/1000,"deg.C")
    sleep(6)
