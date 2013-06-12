import spi
import time

from twisted.python import log

class WS2801():
    def __init__(self):
        self.spi = spi.SPI(0,0)
        self.spi.msh = 1000000

    def updateBlossom(self, blossom):
        for i in range(72):
            self.spi.writebytes(blossom.data[i * 30:i * 30 + 30])
            
        time.sleep(0.001)
