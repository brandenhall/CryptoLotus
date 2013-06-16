import random
import settings

from twisted.python import log


class Paparazzi:

    def __init__(self, flashes=10, color=0xFFFFFF):
        self.flashes = flashes
        self.r = color >> 16 & 0xFF
        self.g = color >> 8 & 0xFF
        self.b = color & 0xFF

    def draw(self, blossom):
        blossom.data = [0] * (settings.LEDS * 3)

        for i in range(self.flashes):
            index = random.randint(0, settings.LEDS - 1)
            blossom.data[index * 3 + 1] = self.r
            blossom.data[index * 3 + 2] = self.g
            blossom.data[index * 3] = self.b
