#!/usr/bin/env python3

import random
import asyncio
import _tm1637
import mraa
import rotary_encoder as renc
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client

CLK = 24
DIO = 23
PIN1 = 8
PIN2 = 10

tm = _tm1637.TM1637(clk=CLK, dio=DIO)


class Tastoma:
    def __init__(self, p1, p2):
        self._enc = renc.RotaryEncoder(p1, p2, renc.LATCHMODE['FOUR3'])


def isr_routine(gpio):
    enc._enc.tick()


def filter_handler(address, *args):
    #print(f"{address}: {args}")
    value = int(args[0])
    value = str(value)
    tm.show(value.rjust(4))


dispatcher = Dispatcher()
dispatcher.map("/filter", filter_handler)

IP = '127.0.0.1'
PORT = 7000
IN_PORT = 8000


async def loop():
    """Example main loop that only runs for 10 iterations before finishing"""
    client = udp_client.SimpleUDPClient(IP, PORT)

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
        #print(f"Loop {i}")
        #client.send_message("/filter", random.random())
        # await asyncio.sleep(1)
        enc._enc.tick()
        new_pos = enc._enc.get_position()

        if pos != new_pos:
            direction = int(enc._enc.get_direction())
            print(f"pos: {new_pos}\tdir: {direction}")
            client.send_message("/direction", direction)
            pos = new_pos

        await asyncio.sleep(0.01)


async def init_main():
    server = AsyncIOOSCUDPServer(
        (IP, IN_PORT), dispatcher, asyncio.get_event_loop())

    # Create datagram endpoint and start serving
    transport, protocol = await server.create_serve_endpoint()

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())
