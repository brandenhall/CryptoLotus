import spi

class WS2801():
    def __init__(self):
        spi.openSPI(speed=900000)

    def updateBlossom(self, blossom):
        segments = []
        for i in range(48)
            segments.append(tuple(blossom.data[i * 15:i * 15 + 15]))

        for segment in segments:
            log.msg(segment)
            spi.transfer(segment)