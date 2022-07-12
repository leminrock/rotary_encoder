#!/usr/bin/env python3

import rotaryrencoder as renc
import mraa
from pythonosc import udp_client

IP = '127.0.0.1'
PORT = 7000
PIN1 = 8
PIN2 = 10


class Encoder:
    def __init__(self, p1, p2):
        self.renc = renc.RotaryEncoder(p1, p2, renc.LATCHMODE['FOUR3'])


def isr_routine(gpio):
    enc.renc.tick()


def configure_pin(pin):
    x = mraa.Gpio(pin)
    x.dir(mraa.DIR_IN)
    x.mode(mraa.MODE_PULLUP)
    return x

if __name__ == '__main__':
    client = udp_client.SimpleUDPClient(IP, PORT)

    x = configure_pin(PIN1)
    y = configure_pin(PIN2)
    
    enc = Encoder(x, y)

    x.isr(mraa.EDGE_BOTH, isr_routine, x)
    y.isr(mraa.EDGE_BOTH, isr_routine, y)

    pos = 0

    while True:
        enc.renc.tick()
        new_pos = enc.renc.get_position()

        if pos != new_pos:
            direction = int(enc.renc.get_direction())
            #print(f"pos: {new_pos}\tdir: {direction}")
            client.send_message("/direction", direction)
            pos = new_pos
