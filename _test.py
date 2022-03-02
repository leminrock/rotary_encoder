#!/usr/bin/env python3

import rotary_encoder as renc
import mraa
from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

PIN1 = 11
PIN2 = 13


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
a_pos = 0

names = ["A","B","C","D","E","F"]

with canvas(device) as draw:
    draw.text((30, a_pos), "REVERB", fill="white")

while True:
    enc._enc.tick()
    new_pos = enc._enc.get_position()
    direction = int(enc._enc.get_direction())

    if pos != new_pos:
        print(f"pos: {new_pos}\tdir: {int(enc._enc.get_direction())}")
        pos = new_pos
        if direction == 1:
            a_pos += 1
        else:
            a_pos -= 1
        with canvas(device) as draw:
            for i in range(6):
                draw.text((30, i * 10), names[(a_pos+i)%6], fill="white")


