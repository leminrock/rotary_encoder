#!/usr/bin/env python3

import _tm1637
from pythonosc import dispatcher
from pythonosc import osc_server

IP = '127.0.0.1'
IN_PORT = 8000
CLK = 13
DIO = 11 
ADDRESS = ['/rotary_0', '/rotary_1']

tm = _tm1637.TM1637(clk=CLK, dio=DIO)


def value_handler(unused_addr, *args):
    """callback function"""
    value = args[0]
    #value = str(int(value))
    #tm.show(value.rjust(4))
    value = int(value)
    tm.number(value)

if __name__ == '__main__':

    dispatcher = dispatcher.Dispatcher()
    list(map(lambda x: dispatcher.map(x, value_handler), ADDRESS))

    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
