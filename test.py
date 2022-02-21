#!/usr/bin/env python3

import rotary_encoder as re
import mraa


PIN1 = 11
PIN2 = 13

encoder = re.RotaryEncoder(PIN1, PIN2, re.LATCHMODE['TWO03'])


def isr():
    encoder.tick()


if __name__ == '__main__':
    print("Test with rotary encoder")

    x = mraa.Gpio(PIN1)
    y = mraa.Gpio(PIN2)
    x.dir(mraa.DIR_IN)
    y.dir(mraa.DIR_IN)
    x.isr(mraa.EDGE_BOTH, isr, x)
    y.isr(mraa.EDGE_BOTH, isr, y)

    while True:
        pos = 0
        encoder.tick()
        new_pos = encoder.get_position()
        if pos != new_pos:
            print("pos:", new_pos)
            print(" dir:")
            print(int(encoder.get_direction()))
            pos = new_pos
