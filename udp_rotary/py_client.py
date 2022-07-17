#!/usr/bin/env python3

import mraa
import toml
import rotary_encoder as renc
from pythonosc import udp_client
from colorama import Fore


DEBUG = None
IP = None
IN_PORT = None
CONFIG_PATH = '/rot_config.toml'


def init_config():
    global DEBUG, IP, IN_PORT

    with open(CONFIG_PATH, 'r') as f:
        data = toml.load(f)

    DEBUG = data['debug']['DEBUG']
    IP = data['network']['IP']
    IN_PORT = data['network']['IN_PORT']

    print(DEBUG, IP, IN_PORT)


def debug(txt):
    """debug printing"""
    if DEBUG:
        print(Fore.BLUE + txt + Fore.WHITE)


def isr_routine(encoder):
    """callback function"""
    encoder.tick()


class Encoder:
    """class to manage rotary encoder"""

    def __init__(self, pin1, pin2, latchmode='FOUR3', routine=isr_routine, address=None):
        self.__config(pin1, pin2, latchmode, routine)
        self.pos = 0
        self.address = address

    def __configure_pin(self, pin):
        c_pin = mraa.Gpio(pin)
        c_pin.dir(mraa.DIR_IN)
        c_pin.mode(mraa.MODE_PULLUP)
        return c_pin

    def __config(self, pin1, pin2, latchmode, routine):
        x, y = list(map(self.__configure_pin, [pin1, pin2]))
        self.rot = renc.RotaryEncoder(x, y, renc.LATCHMODE[latchmode])
        list(map(lambda x: x.isr(mraa.EDGE_BOTH, routine, self.rot), [x, y]))

    def update(self, sender_func):
        """call this function every iteration of main loop"""
        self.rot.tick()
        new_pos = self.rot.get_position()

        if self.pos != new_pos:
            direction = int(self.rot.get_direction())
            debug(f"{self.address}, pos: {new_pos}\tdir: {direction}")
            sender_func(self.address, direction)
            self.pos = new_pos


if __name__ == '__main__':
    client = udp_client.SimpleUDPClient(IP, PORT)
    encoders = [
        Encoder(BUTTON0_PIN1, BUTTON0_PIN2, address='/rotary_0'),
        Encoder(BUTTON1_PIN1, BUTTON1_PIN2, address='/rotary_1'),
        Encoder(BUTTON2_PIN1, BUTTON2_PIN2, address='/rotary_2')
    ]

    while True:
        list(map(lambda x: x.update(client.send_message), encoders))
