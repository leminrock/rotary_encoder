#!/usr/bin/env python3

import mraa
import sys
import time

def button_isr_routine(gpio):
    print("button value", gpio.read())


x = mraa.Gpio(3)
x.dir(mraa.DIR_IN)
#x.mode(mraa.MODE_PULLUP)
x.isr(mraa.EDGE_BOTH, button_isr_routine, x)

while True:
    try:
        print(x.read())
        time.sleep(0.25)
    except KeyboardInterrupt:
        sys.exit(0)
