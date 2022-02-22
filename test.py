#!/usr/bin/env python3

import rotary_encoder as renc
import mraa


PIN1 = 11
PIN2 = 13


class Tastoma:
    def __init__(self, p1, p2):
        self._enc = renc.RotaryEncoder(p1, p2, renc.LATCHMODE['TWO03'])


def isr_routine(gpio):
    enc._enc.tick()
    # print(gpio.read())
    # print()
    # print()
    # print(f"pin: {gpio.getPin(True)}\tvalue: {gpio.read()}")
    # print()


print("Test with rotary encoder")
x = mraa.Gpio(PIN1)
y = mraa.Gpio(PIN2)
x.dir(mraa.DIR_IN)
y.dir(mraa.DIR_IN)

enc = Tastoma(x, y)

x.isr(mraa.EDGE_BOTH, isr_routine, x)
y.isr(mraa.EDGE_BOTH, isr_routine, y)


while True:
    pos = 0
    enc._enc.tick()
    new_pos = enc._enc.get_position()
    if pos != new_pos:
        print("pos:", new_pos)
        print(" dir:")
        print(int(enc._enc.get_direction()))
        pos = new_pos
