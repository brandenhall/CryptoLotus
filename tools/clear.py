import spi

halves = 24

s = spi.SPI(0,0)
s.msh = 1000000
colors = [0,0,0]

for i in range(halves):
    s.writebytes(colors * 10)
    s.writebytes(colors * 10)
    s.writebytes(colors * 10)
