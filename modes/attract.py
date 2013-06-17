import settings
import random
import colorsys
import math

from os import listdir
from os.path import isfile, join
from twisted.python import log

from blossom.patterns import SlitScan

class AttractMode:
    
    def __init__(self, lotus):
        self.lotus = lotus
        self.patterns = []
        self.frame = 0
        self.lilypad_frame = 0
        self.lilypad = 0
        self.lilypad_hue = 0.0

        images = [f for f in listdir(settings.ATTRACT_PATH) if isfile(join(settings.ATTRACT_PATH, f))]
        for image in images:
            self.patterns.append(SlitScan(join(settings.ATTRACT_PATH, image), 1))

    def startMode(self):
        for lilypad in self.lotus.lilypads:
            lilypad.setColor(0)

        self.lotus.blossom.clear()
        self.frame = random.randint(settings.MIN_ATTRACT_FRAMES, settings.MAX_ATTRACT_FRAMES)
        self.transition = 64
        self.back_pattern = random.choice(self.patterns)
        self.front_pattern = None
        self.is_transitioning = False

    def stopMode(self):
        pass

    def update(self):
        if any(lilypad.active for lilypad in self.lotus.lilypads):
            self.lotus.changeMode(self.lotus.login_mode)

        elif self.is_transitioning:
            if self.transition == 0:
                self.back_pattern = self.front_pattern
                self.lotus.blossom.data = self.back_pattern.draw()
                self.frame = random.randint(settings.MIN_ATTRACT_FRAMES, settings.MAX_ATTRACT_FRAMES)
                self.frame -= 1
                self.front_pattern = None
                self.is_transitioning = False

            else:
                inv = 4 * self.transition + 1
                alpha = 257 - inv

                back_buffer = self.back_pattern.draw()
                front_buffer = self.front_pattern.draw()

                for i in range(len(self.lotus.blossom.data)):
                    self.lotus.blossom.data[i] = (front_buffer[i] * alpha + back_buffer[i] * inv) >> 8

                self.transition -= 1

        else:
            self.lotus.blossom.data = self.back_pattern.draw()
            self.frame -= 1

            # done with pattern, pick the next one
            if self.frame == 0:
                self.is_transitioning = True
                self.front_pattern = random.choice(self.patterns)
                self.transition = 64

        # make the lilypads spin
        if self.lilypad_frame == 0:
            self.lilypad_hue = math.fmod(self.lilypad_hue, 1)
            rgb = colorsys.hsv_to_rgb(self.lilypad_hue, 1, settings.ATTRACT_LILYPAD_BRIGHTNESS)

            self.lilypad_hue += settings.ATTRACT_LILYPAD_HUE_STEP
            self.lilypad += 1
            self.lilypad %= settings.LILYPADS


            for i, lilypad in enumerate(self.lotus.lilypads):
                if i != self.lilypad:
                    lilypad.setColor(0)
                else:
                    lilypad.setColor(int(rgb[0] * 255) << 16 | int(rgb[1] * 255) << 8 | int(rgb[2] * 255))

        self.lilypad_frame += 1

        if self.lilypad_frame == settings.ATTRACT_LILYPAD_RATE:
            self.lilypad_frame = 0
        