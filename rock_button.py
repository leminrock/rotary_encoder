import mraa


def isr_routine(gpio):
    print("button value", gpio.read())


x = mraa.Gpio(12)
x.dir(mraa.DIR_IN)
x.isr(mraa.EDGE_BOTH, isr_routine, x)
