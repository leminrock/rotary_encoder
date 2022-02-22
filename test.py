#!/usr/bin/env python3

import rotary_encoder as re
import mraa


PIN1 = 11
PIN2 = 13

#encoder = re.RotaryEncoder(PIN1, PIN2, re.LATCHMODE['TWO03'])

enc = 0

def isr_routine():
    enc.tick()


print("Test with rotary encoder")
x = mraa.Gpio(PIN1)
y = mraa.Gpio(PIN2)
x.dir(mraa.DIR_IN)
y.dir(mraa.DIR_IN)
enc = re.RotaryEncoder(x, y, re.LATCHMODE['TWO03'])
x.isr(mraa.EDGE_BOTH, isr_routine, x)
y.isr(mraa.EDGE_BOTH, isr_routine, y)


while True:
    pos = 0
    enc.tick()
    new_pos = enc.get_position()
    if pos != new_pos:
        print("pos:", new_pos)
        print(" dir:")
        print(int(enc.get_direction()))
        pos = new_pos
