import settings
import random
import colorsys
import math
import RPi.GPIO as GPIO

from os import listdir
from os.path import isfile, join
from twisted.python import log

from twisted.internet import reactor


from blossom.patterns import SlitScan, Paparazzi, Black

ATTRACT_MODE = "attract"
TRANSITION_MODE = "transition"
FOREPLAY_MODE = "foreplay"
BLOSSOM_MODE = "blossom"

class AttractMode:
    
    def __init__(self, lotus):
        self.lotus = lotus
        self.patterns = []
        self.rewards = []
        self.frame = 0
        self.counter = 0
        self.lilypad_frame = 0
        self.lilypad = 0
        self.lilypad_hue = 0.0
        self.paparazzi = Paparazzi()
        self.black = Black()
        self.attract_count = 0
        self.mode = ATTRACT_MODE

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)
        GPIO.output(12, 0)
        GPIO.output(16, 0) 

        images = [f for f in listdir(settings.ATTRACT_PATH) if isfile(join(settings.ATTRACT_PATH, f))]
        for image in images:
            self.patterns.append(SlitScan(join(settings.ATTRACT_PATH, image), 1))

        images = [f for f in listdir(settings.REWARD_PATH) if isfile(join(settings.REWARD_PATH, f))]
        for image in images:
            self.rewards.append(SlitScan(join(settings.REWARD_PATH, image), 1))

    def openLotus(self):
        GPIO.output(12, 1)
        GPIO.output(16, 0)

    def closeLotus(self):
        GPIO.output(12, 0)
        GPIO.output(16, 1)
        self.blossom_pattern.speed = -1

    def showLotus(self):
        GPIO.output(12, 0)
        GPIO.output(16, 0) 

    def hideLotus(self):
        GPIO.output(12, 0)
        GPIO.output(16, 0) 
        self.mode = ATTRACT_MODE
        self.front_pattern = self.black
        self.back_pattern = self.black
        self.frame = 0
        self.attract_count = -1

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
        GPIO.output(12, 0)
        GPIO.output(16, 0) 

    def update(self):
        if self.mode == BLOSSOM_MODE:
            self.lotus.blossom.data = self.blossom_pattern.draw()

        elif self.mode == FOREPLAY_MODE:
            self.lotus.blossom.data = self.paparazzi.draw()
            self.frame -= 1

            if self.frame == 0:
                self.mode = BLOSSOM_MODE
                self.openLotus()
                reactor.callLater(settings.BLOSSOM_MOVE_TIME, self.showLotus)
                reactor.callLater(settings.BLOSSOM_MOVE_TIME + settings.BLOSSOM_SHOW_TIME, self.closeLotus)
                reactor.callLater((settings.BLOSSOM_MOVE_TIME * 2) + settings.BLOSSOM_SHOW_TIME, self.hideLotus)
                self.blossom_pattern = random.choice(self.rewards)
                self.blossom_pattern.speed = 3


        elif self.mode == TRANSITION_MODE:
            if self.transition == 0:
                self.back_pattern = self.front_pattern
                self.lotus.blossom.data = self.back_pattern.draw()
                self.frame = random.randint(settings.MIN_ATTRACT_FRAMES, settings.MAX_ATTRACT_FRAMES)
                self.frame -= 1
                self.front_pattern = None
                self.mode = ATTRACT_MODE

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
                self.attract_count += 1

                if self.attract_count == settings.BLOSSOM_RATE:
                    self.mode = FOREPLAY_MODE
                    self.frame = settings.FOREPLAY_FRAMES

                else:
                    self.mode = TRANSITION_MODE
                    self.front_pattern = random.choice(self.patterns)
                    while self.front_pattern == self.back_pattern:
                        self.front_pattern = random.choice(self.patterns)
                    self.front_pattern.speed = random.choice([-1, 1])

                    self.transition = 64

        # make the lilypads spin
        # if self.lilypad_frame == 0:
        #     self.lilypad_hue = math.fmod(self.lilypad_hue, 1)
        #     rgb = colorsys.hsv_to_rgb(self.lilypad_hue, 1, settings.ATTRACT_LILYPAD_BRIGHTNESS)

        #     self.lilypad_hue += settings.ATTRACT_LILYPAD_HUE_STEP
        #     self.lilypad += 1
        #     self.lilypad %= settings.LILYPADS


        #     for i, lilypad in enumerate(self.lotus.lilypads):
        #         if i != self.lilypad:
        #             lilypad.setColor(0)
        #         else:
        #             lilypad.setColor(int(rgb[0] * 255) << 16 | int(rgb[1] * 255) << 8 | int(rgb[2] * 255))

        # self.lilypad_frame += 1

        # if self.lilypad_frame == settings.ATTRACT_LILYPAD_RATE:
        #     self.lilypad_frame = 0
        