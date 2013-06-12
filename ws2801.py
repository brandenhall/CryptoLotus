import spi

class WS2801():
    def __init__(self):
        self.spi = spi.SPI(0,0)
        self.spi.msh = 1000000

    def updateBlossom(self, blossom):
        segments = []
        for i in range(48)
            segments.append(blossom.data[i * 15:i * 15 + 15])

        for segment in segments:
            self.spi.writebytes(segment)
