import spi

class WS2801():
    def __init__(self):
        spi.openSPI(speed=1000000)

    def updateBlossom(self, blossom):
        data = []
        for i in range(12):
            for j in range(60):
                pixel = blossom[i * 60 + j]
                data.append(pixel & 0xFF)
                data.append(pixel >> 8 & 0xFF)
                data.append(pixel >> 16 & 0xFF)
            spi.transfer(tuple(data))