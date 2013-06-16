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

    @timecall(immediate=True)
    def draw(self):
        index = 0
        half_petal = settings.LEDS_PER_PETAL / 2
        p2 = settings.PETALS * 2
        right = self.offset * p2
        left = right + 720


        for i in range(settings.PETALS):
            i2 = i * 2

            for j in range(half_petal):
                jp2 = p2 * j

                # left half of the petal
                pixel = ((left - jp2 + i2) % self.image_size) * 3
                self.data[index * 3 + 1] = self.raw_data[pixel]
                self.data[index * 3 + 2] = self.raw_data[pixel + 1]
                self.data[index * 3] = self.raw_data[pixel + 2]

                # right half of the petal
                pixel = ((right + jp2 + i2 + 1) % self.image_size) * 3
                self.data[(index + half_petal) * 3 + 1] = self.raw_data[pixel]
                self.data[(index + half_petal) * 3 + 2] = self.raw_data[pixel + 1]
                self.data[(index + half_petal) * 3] = self.raw_data[pixel + 2]

                index += 1

            index += half_petal

        self.offset += self.speed

        if self.offset < 0:
            self.offset = self.height + self.offset

        if self.offset >= self.height:
            self.offset -= self.height

        return self.data

# import settings

# from PIL import Image
# from twisted.python import log

# class SlitScan:

#     def __init__(self, filename, speed=1):
#         self.im = Image.open(filename)
#         self.speed = speed
#         self.offset = 0
#         (self.width, self.height) = self.im.size
#         self.raw_data = self.im.getdata()
#         self.len_raw_data = len(self.raw_data)
#         self.data = [0,0,0] * settings.LEDS

#     def draw(self):
#         index = 0
#         half_petal = settings.LEDS_PER_PETAL / 2
#         half_petals = settings.PETALS * 2

#         for i in range(settings.PETALS):

#             for j in range(half_petal):

#                 # left half of the petal
#                 pixel = ((self.offset * settings.PETALS * 2) + 720  - (j * settings.PETALS * 2) + (i * 2)) % self.len_raw_data
#                 self.data[index * 3 + 1] = self.raw_data[pixel][0]
#                 self.data[index * 3 + 2] = self.raw_data[pixel][1]
#                 self.data[index * 3] = self.raw_data[pixel][2]

#                 # right half of the petal
#                 pixel = ((self.offset * settings.PETALS * 2) + (j * settings.PETALS * 2) + (i * 2) + 1) % self.len_raw_data
#                 self.data[(index + half_petal) * 3 + 1] = self.raw_data[pixel][0]
#                 self.data[(index + half_petal) * 3 + 2] = self.raw_data[pixel][1]
#                 self.data[(index + half_petal) * 3] = self.raw_data[pixel][2]

#                 index += 1

#             index += half_petal

#         self.offset += self.speed

#         if self.offset < 0:
#             self.offset = self.height + self.offset

#         if self.offset >= self.height:
#             self.offset -= self.height

#         return self.data

