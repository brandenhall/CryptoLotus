import random


class Paparazzi:

    def __init__(self, num_lights=10, color=0xFFFFFF):
        self.num_lights = num_lights
        self.color = color
        self.loop_index = 0

    def draw(self, blossom):
        for i in range(720):
            blossom[i] = 0

        for i in range(self.num_lights):
            blossom[random.randint(0, 719)] = self.color
