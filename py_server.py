#!/usr/bin/env python3

import _tm1637
from pythonosc import dispatcher
from pythonosc import osc_server

IP = '127.0.0.1'
IN_PORT = 8000
CLK = 24
DIO = 23

tm = _tm1637.TM1637(clk=CLK, dio=DIO)


def value_handler(unused_addr, *args):
    value = args[0]
    value = str(int(value))
    tm.show(value.rjust(4))


if __name__ == '__main__':

    dispatcher = dispatcher.Dispatcher()
    dispatcher.map("/filter", value_handler)

    server = osc_server.ThreadingOSCUDPServer((IP, IN_PORT), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()

    """
    while True:
        client.send_message("/filter", random.random())
        print("send")
        time.sleep(1)
    """
