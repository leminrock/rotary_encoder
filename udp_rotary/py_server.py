#!/usr/bin/env python3

import toml
import _tm1637
from pythonosc import dispatcher
from pythonosc import osc_server


#tm = _tm1637.TM1637(clk=CLK, dio=DIO)

IP = None
IN_PORT = None
ADDRESS = None
CLK = None
DIO = None
TM = None
CONFIG_PATH = './rot_config.toml'


def init_config():
    global IP, IN_PORT, ADDRESS, CLK, DIO

    with open(CONFIG_PATH, 'r') as f:
        data = toml.load(f)

    IP = data['network']['IP']
    IN_PORT = data['network']['IN_PORT']
    #ENCODERS = [data['encoders'][enc] for enc in data['encoders']]
    ADDRESS = [data['encoders'][enc]['ADDRESS'] for enc in data['encoders']]
    CLK = data['i2c']['CLK']
    DIO = data['i2c']['DIO']


def value_handler(unused_addr, *args):
    """callback function"""
    value = args[0]
    #value = str(int(value))
    # tm.show(value.rjust(4))
    value = int(value)
    tm.number(value)


if __name__ == '__main__':
    init_config()
    TM = _tm1637.TM1637(clk=CLK, dio=DIO)
    dispatcher = dispatcher.Dispatcher()
    list(map(lambda x: dispatcher.map(x, value_handler), ADDRESS))

    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
