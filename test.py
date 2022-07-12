#!/usr/bin/env python3

import rotary_encoder as renc
import mraa


PIN1 = 8
PIN2 = 10


class Tastoma:
    def __init__(self, p1, p2):
        self._enc = renc.RotaryEncoder(p1, p2, renc.LATCHMODE['FOUR3'])


def isr_routine(gpio):
    enc._enc.tick()


print("Test with rotary encoder")
x = mraa.Gpio(PIN1)
y = mraa.Gpio(PIN2)
x.dir(mraa.DIR_IN)
y.dir(mraa.DIR_IN)
x.mode(mraa.MODE_PULLUP)
y.mode(mraa.MODE_PULLUP)
enc = Tastoma(x, y)

x.isr(mraa.EDGE_BOTH, isr_routine, x)
y.isr(mraa.EDGE_BOTH, isr_routine, y)

pos = 0
lastdir = None

while True:
    enc._enc.tick()
    new_pos = enc._enc.get_position()
    if pos != new_pos:
        print(f"pos: {new_pos}\tdir: {int(enc._enc.get_direction())}")
        pos = new_pos

