import settings
import random

from os import listdir
from os.path import isfile, join
from twisted.python import log

from blossom.patterns import SlitScan

class AttractMode:
    
    def __init__(self, lotus):
        self.lotus = lotus
        self.patterns = []
        self.frame = 0

        images = [f for f in listdir(settings.ATTRACT_PATH) if isfile(join(settings.ATTRACT_PATH, f))]
        for image in images:
            self.patterns.append(SlitScan(join(settings.ATTRACT_PATH, image), 2))
            self.patterns.append(SlitScan(join(settings.ATTRACT_PATH, image), -2))

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
        if self.is_transitioning:
            if self.transition == 0:
                self.back_pattern = self.front_pattern
                self.lotus.blossom.data = self.back_pattern.draw()
                self.frame = random.randint(settings.MIN_ATTRACT_FRAMES, settings.MAX_ATTRACT_FRAMES)
                self.frame -= 1
                self.front_pattern = None
                self.is_transitioning = False

            else:
                inv = 2 * self.transition + 1
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
                log.msg("CHANGE PATTERN!")
                self.is_transitioning = True
                self.front_pattern = random.choice(self.patterns)
                self.transition = 128
        