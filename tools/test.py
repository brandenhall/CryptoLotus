import spi
import time

halves = 24

s = spi.SPI(0,0)
s.msh = 1000000
blue =   [255,0,0]
red = [0,255,0]
green =  [0,0,255]

while True:
    s.writebytes(red * 720)
    time.sleep(5)
    s.writebytes(green * 720)
    time.sleep(5)
    s.writebytes(blue * 720)
    time.sleep(5)
