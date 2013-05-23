from twisted.python import log

NUM_PETALS = 12
NUM_LIGHTS_PER_PETAL = 60


class Petal:

    def __init__(self):
        self.is_dirty = False
        self._pixels = [0] * NUM_LIGHTS_PER_PETAL

    def __getitem__(self, key):
        return self._pixels[key]

    def __setitem__(self, key, value):
        self.is_dirty = True
        self._pixels[key] = value

    def serialize(self):
        self.is_dirty = False
        return self._pixels


class Blossom:

    def __init__(self, lotus):
        self.lotus = lotus
        self.petals = []

        for i in range(NUM_PETALS):
            self.petals.append(Petal())

    def __getitem__(self, index):
        petal_index = index / NUM_LIGHTS_PER_PETAL
        return self.petals[petal_index][index - petal_index * NUM_LIGHTS_PER_PETAL]

    def __setitem__(self, index, value):
        petal_index = index / NUM_LIGHTS_PER_PETAL
        self.petals[petal_index][index - petal_index * NUM_LIGHTS_PER_PETAL] = value

    def update(self):
        self.lotus.updateBlossom(self)

    def serialize(self):
        result = []
        for petal in self.petals:
            result.extend(petal.serialize())

        return result
