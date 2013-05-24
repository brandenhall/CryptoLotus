import settings

from twisted.python import log


class Blossom:

    def __init__(self, lotus):
        self.lotus = lotus
        self.data = []
        self.data = [0] * (settings.LEDS * 3)

    def update(self):
        self.lotus.updateBlossom(self)
