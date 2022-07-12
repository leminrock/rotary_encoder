#!/usr/bin/env python3

import random
import asyncio
import _tm1637
from pythonosc.osc_server import AsyncIOOSCUDPServer
from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client

CLK = 24
DIO = 23

tm = _tm1637.TM1637(clk=CLK, dio=DIO)


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

    while True:
        #print(f"Loop {i}")
        client.send_message("/filter", random.random())
        await asyncio.sleep(1)


async def init_main():
    server = AsyncIOOSCUDPServer(
        (IP, IN_PORT), dispatcher, asyncio.get_event_loop())

    # Create datagram endpoint and start serving
    transport, protocol = await server.create_serve_endpoint()

    await loop()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())
