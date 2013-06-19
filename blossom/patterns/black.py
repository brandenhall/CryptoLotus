import settings

class Black:

    def __init__(self):
        self.data = [0] * (settings.LEDS * 3)

    def draw(self):
        return self.data
