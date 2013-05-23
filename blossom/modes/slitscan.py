from PIL import Image

from twisted.python import log

class SlitScan:

    def __init__(self, filename, speed=1):
        self.im = Image.open(filename)
        self.speed = speed
        self.offset = 0
        (self.width, self.height) = self.im.size
        self.raw_data = self.im.getdata()

    def draw(self, blossom):
        index = 0

        for i, petal in enumerate(blossom.petals):

            for j in range(30):
                pixel = (self.offset * 24) + 720  - (j * 24) + (i * 2)
                if pixel > len(self.raw_data) - 1:
                    pixel -= len(self.raw_data)
                if pixel < 0:
                    pixel += len(self.raw_data)

                blossom[index] = self.raw_data[pixel][2] << 16 | self.raw_data[pixel][1] << 8 | self.raw_data[pixel][0]

                index += 1

            for j in range(30):
                pixel = (self.offset * 24) + (j * 24) + (i * 2) + 1
                if pixel > len(self.raw_data) - 1:
                    pixel -= len(self.raw_data)
                if pixel < 0:
                    pixel += len(self.raw_data)

                blossom[index] = self.raw_data[pixel][2] << 16 | self.raw_data[pixel][1] << 8 | self.raw_data[pixel][0]
                index += 1

        self.offset += self.speed

        if self.offset < 0:
            self.offset = self.height + self.offset

        if self.offset >= self.height:
            self.offset -= self.height

