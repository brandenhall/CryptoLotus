import settings
import colorsys
import math

from twisted.python import log


class ColorWheel:
    def __init__(self, speed, brightness=0.5):
        self.offset = 0
        self.speed = speed
        self.brightness = brightness
        self.step = 1.0 / (settings.LEDS + 1)

    def draw(self, blossom):
        for i in range(settings.LEDS):
            hue = math.fmod(self.offset + (i * self.step), 1)
            rgb = colorsys.hsv_to_rgb(hue, 1, self.brightness)
            blossom.data[i * 3 + 2] = int(rgb[0] * 255)
            blossom.data[i * 3] = int(rgb[1] * 255)
            blossom.data[i * 3 + 1] = int(rgb[2] * 255)

        self.offset = math.fmod(self.offset + self.speed, 1)