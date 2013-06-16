import spi
import time

from profilehooks import timecall

class WS2801():
    def __init__(self):
        self.spi = spi.SPI(0,0)
        self.spi.msh = 1950000
    
    def updateBlossom(self, blossom):
        self.spi.writebytes(blossom.data)
