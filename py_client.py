import rotary_encoder as renc
import mraa
from pythonosc import udp_client

IP = '127.0.0.1'
PORT = 7000
PIN1 = 8
PIN2 = 10


class Tastoma:
    def __init__(self, p1, p2):
        self._enc = renc.RotaryEncoder(p1, p2, renc.LATCHMODE['FOUR3'])


def isr_routine(gpio):
    enc._enc.tick()


if __name__ == '__main__':
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

    """
    while True:
        client.send_message("/filter", random.random())
        print("send")
        time.sleep(1)
    """

    while True:
        enc._enc.tick()
        new_pos = enc._enc.get_position()
        if pos != new_pos:
            direction = int(enc._enc.get_direction())
            print(f"pos: {new_pos}\tdir: {direction}")
            client.send_message("/direction", direction)
            pos = new_pos
