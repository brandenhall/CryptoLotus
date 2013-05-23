class ColorWheel:
    def __init__(self):
        self.loop_index = 0

    def makeColor(self, r, g, b):
        return r << 16 | g << 8 | b

    def colorWheel(self, pos):
        if pos < 85:
            return self.makeColor(pos * 3, 255 - pos * 3, 0)

        elif pos < 170:
            pos -= 85
            return self.makeColor(255 - pos * 3, 0, pos * 3)

        else:
            pos -= 170
            return self.makeColor(0, pos * 3, 255 - pos * 3)

    def draw(self, blossom):
        for i in range(720):
            blossom[i] = self.colorWheel(((i * 256 / 256) + self.loop_index) % 256)

        self.loop_index += 1
