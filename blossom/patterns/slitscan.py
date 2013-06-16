import settings

from PIL import Image
from twisted.python import log

from profilehooks import timecall


class SlitScan:

    def __init__(self, filename, speed=1):
        self.im = Image.open(filename)
        self.speed = speed
        self.offset = 0
        (self.width, self.height) = self.im.size

        self.raw_data = []
        image_data = self.im.getdata()
        self.image_size = len(image_data)

        for pixel in image_data:
            self.raw_data.extend(pixel)

        self.data = [0, 0, 0] * settings.LEDS

    @timecall
    def draw(self):
        index = 0
        half_petal = settings.LEDS_PER_PETAL / 2
        offset = self.offset
        petals = settings.PETALS
        image_size = self.image_size
        data = self.data
        raw_data = self.raw_data
        op2 = offset * petals * 2

        i = 0
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2
            
            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 1
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 2
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 3
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 4
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 5
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 6
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 7
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 8
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 9
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 10
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        index += half_petal
        i = 11
        i2 = i * 2
        for j in range(half_petal):
            jp2 = j * petals * 2

            # left half of the petal
            pixel = ((op2 + 720 - jp2 + i2) % image_size) * 3
            data[index * 3 + 1] = raw_data[pixel]
            data[index * 3 + 2] = raw_data[pixel + 1]
            data[index * 3] = raw_data[pixel + 2]

            # right half of the petal
            pixel = ((op2 + jp2 + i2 + 1) % image_size) * 3
            data[(index + half_petal) * 3 + 1] = raw_data[pixel]
            data[(index + half_petal) * 3 + 2] = raw_data[pixel + 1]
            data[(index + half_petal) * 3] = raw_data[pixel + 2]

            index += 1

        self.offset += self.speed

        if self.offset < 0:
            self.offset = self.height + self.offset

        if self.offset >= self.height:
            self.offset -= self.height

        return self.data