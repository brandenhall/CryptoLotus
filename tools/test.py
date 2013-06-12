import spi
import time

halves = 24

s = spi.SPI(0,0)
s.msh = 1000000
red =   [255,0,0]
green = [0,255,0]
blue =  [0,0,255]

while True:
    for i in range(halves):
        s.writebytes(red * 10)
        s.writebytes(red * 10)
        s.writebytes(red * 10)

    time.sleep(5)

    for i in range(halves):
        s.writebytes(green * 10)
        s.writebytes(green * 10)
        s.writebytes(green * 10)

    time.sleep(5)

    for i in range(halves):
        s.writebytes(blue * 10)
        s.writebytes(blue * 10)
        s.writebytes(blue * 10)

    time.sleep(5)
