#!/usr/bin/env python3

import time
import random
import asyncio
from pythonosc import udp_client
from pythonosc import dispatcher
from pythonosc import osc_server

IP = '127.0.0.1'
PORT = 7000
IN_PORT = 8000


def print_volume_handler(unused_addr, args, volume):
    print("[{0}] ~ {1}".format(args[0], volume))


if __name__ == '__main__':
    client = udp_client.SimpleUDPClient(IP, PORT)

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", print)

    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

    while True:
        client.send_message("/filter", random.random())
        print("send")
        time.sleep(1)
