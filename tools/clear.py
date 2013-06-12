import spi
halves = 24

spi.openSPI(speed=800000)
colors = (0,0,0,0,0,0,0,0,0)

for i in range(halves):
    spi.transfer(colors * 10)