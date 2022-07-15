#!/usr/bin/env python3

import rotary_rencoder as renc
import mraa
from pythonosc import udp_client
from colorama import Fore

DEBUG = 1
IP = '127.0.0.1'
PORT = 7000
PIN1 = 8
PIN2 = 10


def debug(txt):
    if DEBUG:
        print(Fore.BLUE + txt + Fore.WHITE)

def isr_routine(encoder):
    encoder.tick()


def configure_pin(pin):
    c_pin = mraa.Gpio(pin)
    c_pin.dir(mraa.DIR_IN)
    c_pin.mode(mraa.MODE_PULLUP)
    return c_pin


if __name__ == '__main__':
    client = udp_client.SimpleUDPClient(IP, PORT)

    x = configure_pin(PIN1)
    y = configure_pin(PIN2)
    
    enc = renc.RotaryEncoder(x, y, renc.LATCHMODE['FOUR3'])

    x.isr(mraa.EDGE_BOTH, isr_routine, enc)
    y.isr(mraa.EDGE_BOTH, isr_routine, enc)

    pos = 0

    while True:
        enc.tick()
        new_pos = enc.get_position()

        if pos != new_pos:
            direction = int(enc.get_direction())
            debug(f"pos: {new_pos}\tdir: {direction}")
            client.send_message("/direction", direction)
            pos = new_pos
