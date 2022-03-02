#!/usr/bin/env python3

import sys
import mraa
import rotary_encoder as renc

p1 = int(sys.argv[1])
p2 = int(sys.argv[2])


def isr_routine(gpio):
    encoder.tick()

def but_routine(gpio):
    print("activate gpio with value", gpio.read())

PIN1 = p1
PIN2 = p2
PIN3 = 12

x = mraa.Gpio(PIN1)
y = mraa.Gpio(PIN2)
z = mraa.Gpio(PIN3)
x.dir(mraa.DIR_IN)
y.dir(mraa.DIR_IN)
z.dir(mraa.DIR_IN)

encoder = renc.RotaryEncoder(x, y, renc.LATCHMODE['FOUR0'])

x.isr(mraa.EDGE_BOTH, isr_routine, x)
y.isr(mraa.EDGE_BOTH, isr_routine, y)
z.isr(mraa.EDGE_BOTH, but_routine, z)


m = 50  # fattore di moltiplicazione
longCutoff = 50
shortCutoff = 5
a = (m - 1) / (shortCutoff - longCutoff)
b = 1 - longCutoff * a
lastPos = 0

while True:
    encoder.tick()
    newPos = encoder.get_position()
    if lastPos != newPos:
        ms = encoder.get_millis_between_rotations()

        if ms < longCutoff:
            if ms < shortCutoff:
                ms = shortCutoff

            ticksActual_float = a * ms + b
            # print(ticksActual_float)

            deltaTicks = int(ticksActual_float) * (newPos - lastPos)
            # print(deltaTicks)

            newPos = newPos + deltaTicks
            encoder.set_position(newPos)

        print(newPos, 'ms:', ms)
        lastPos = newPos
