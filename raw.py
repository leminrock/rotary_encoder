#!/usr/bin/env python3

import time
import mraa

pin1 = 11
pin2 = 13

p1 = mraa.Gpio(pin1)
p2 = mraa.Gpio(pin2)
p1.dir(mraa.DIR_IN)
p2.dir(mraa.DIR_IN)
p1.mode(mraa.MODE_PULLUP)
p1.mode(mraa.MODE_PULLUP)

while True:
    print(f"p1: {p1.read()}")
    print(f"p2: {p2.read()}")
