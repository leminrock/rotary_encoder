import mraa

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


class RotaryEncoder(Object):
    def __init__(self, pin1, pin2, mode=LATCHMODE['FOUR0']):
        self._pin1
        self._pin2
        self._mode

        # pinMode(pin1, INPUT_PULLUP);
        # pinMode(pin2, INPUT_PULLUP);
        self._pin1 = mraa.Gpio(pin1)
        self._pin2 = mraa.Gpio(pin2)
        self._pin1.dir(mraa.DIR_IN)
        self._pin2.dir(mraa.DIR_IN)

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
            self._positionExtPrev = self._positionExt;
        elif (self._positionExtPrev < self._positionExt) {
            ret = DIRECTION['CLOCKWISE']
            self._positionExtPrev = self._positionExt
        else:
            ret = DIRECTION['NOROTATION']
            self._positionExtPrev = self._positionExt

        return ret

    def set_position(self, new_pos):
        pass

    def tick(self):
        pass

    def get_millis_between_rotations(self):
        pass

    def get_RPM(self):
        pass
