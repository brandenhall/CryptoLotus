import spi
import time

halves = 24

spi.openSPI(speed=1000000)
red =   (255,0,0,255,0,0,255,0,0,255,0,0)
green = (0,255,0,0,255,0,0,255,0,0,255,0)
blue =  (0,0,255,0,0,255,0,0,255,0,0,255)

while True:
    for i in range(halves):
        spi.transfer(red * 10)

    time.sleep(5)

    for i in range(halves):
        spi.transfer(green * 10)

    time.sleep(5)

    for i in range(halves):
        spi.transfer(blue * 10)

    time.sleep(5)
