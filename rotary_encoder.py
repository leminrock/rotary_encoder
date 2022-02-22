import mraa
import time

DIRECTION = {
    'NOROTATION': 0,
    'CLOCKWISE': 1,
    'COUNTERCLOCKWISE': -1
}

LATCHMODE = {
    'FOUR3': 1,
    'FOUR0': 2,
    'TWO03': 3
}

LATCH0 = 0
LATCH3 = 3
KNOBDIR = [0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0]


def millis():
    return int(time.time() * 1000)


class RotaryEncoder(object):
    def __init__(self, pin1, pin2, mode=LATCHMODE['FOUR0']):
        self._pin1 = pin1
        self._pin2 = pin2
        self._mode = mode

        # pinMode(pin1, INPUT_PULLUP)
        # pinMode(pin2, INPUT_PULLUP)
        # self._pin1 = mraa.Gpio(pin1)
        # self._pin2 = mraa.Gpio(pin2)
        # self._pin1.dir(mraa.DIR_IN)
        # self._pin2.dir(mraa.DIR_IN)

        self._oldState = None
        self._position = 0
        self._positionExt = 0
        self._positionExtPrev = 0
        self._positionExtTime = None
        self._positionExtTimePrev = None

        sig1 = self._pin1.read()
        sig2 = self._pin2.read()
        self._oldState = sig1 | (sig2 << 1)

    def get_position(self):
        return self._positionExt

    def get_direction(self):
        ret = DIRECTION['NOROTATION']

        if self._positionExtPrev > self._positionExt:
            ret = DIRECTION['COUNTERCLOCKWISE']
            self._positionExtPrev = self._positionExt
        elif self._positionExtPrev < self._positionExt:
              ret = DIRECTION['CLOCKWISE']
              self._positionExtPrev = self._positionExt
        else:
              ret = DIRECTION['NOROTATION']
              self._positionExtPrev = self._positionExt

        return ret

    def set_position(self, new_pos):
        if self._mode == LATCHMODE['FOUR0']:
            self._position = ((new_pos << 2) | (self._position & 3))
            self._positionExt = new_pos
            self._positionExtPrev = new_pos
        elif self._mode == LATCHMODE['TWO03']:
            self._position = ((new_pos << 1) | (self._position & 1))
            self._positionExt = new_pos
            self._positionExtPrev = new_pos
        else:
            pass

    def tick(self):
        sig1 = self._pin1.read()
        sig2 = self._pin2.read()
        this_state = sig1 | (sig2 << 1)

        if self._oldState != this_state:
            self._position += KNOBDIR[this_state | (self._oldState << 2)]
            self._oldState = this_state

            if self._mode == LATCHMODE['FOUR3']:
                if this_state == LATCH3:
                    # The hardware has 4 steps with a latch on the input state 3
                    self._positionExt = self._position >> 2
                    self._positionExtTimePrev = self._positionExtTime
                    self._positionExtTime = millis()  # TODO: GET TIME IN MILLISECONDS
                elif self._mode == LATCHMODE['FOUR0']:
                    if this_state == LATCH0:
                        # The hardware has 4 steps with a latch on the input state 0
                        self._positionExt = self._position >> 2
                        self._positionExtTimePrev = self._positionExtTime
                        self._positionExtTime = millis()  # TODO: GET TIME IN MILLISECONDS
                else:
                    if (this_state == LATCH0) or (this_state == LATCH3):
                        # The hardware has 2 steps with a latch on the input state 0 and 3
                        self._positionExt = self._position >> 1
                        self._positionExtTimePrev = self._positionExtTime
                        self._positionExtTime = millis()

    def get_millis_between_rotations(self):
        return self._positionExtTime - self._positionExtTimePrev

    def get_RPM(self):
        timeBetweenLastPositions=self._positionExtTime - self._positionExtTimePrev
        timeToLastPosition=millis() - self._positionExtTime
        t=max(timeBetweenLastPositions, timeToLastPosition)
        return 60000.0 / float(t * 20)
