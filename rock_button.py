#!/usr/bin/env python3

import mraa
import sys
import time

def button_isr_routine(gpio):
    print("button value", gpio.read())


#if int(sys.argv[1])
PIN = 8
print("pin:",8)
x = mraa.Gpio(PIN)
x.dir(mraa.DIR_IN)
x.mode(mraa.MODE_PULLDOWN)
x.isr(mraa.EDGE_BOTH, button_isr_routine, x)
"""
while True:
    try:
        print(x.read())
        time.sleep(0.2)
    except KeyboardInterrupt:
        sys.exit(0)
"""
