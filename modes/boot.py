import settings

from twisted.python import log

class BootMode:
    
    def __init__(self, lotus):
        self.lotus = lotus
        self.frame = 0

    def startMode(self):
        for lilypad in self.lotus.lilypads:
            lilypad.setColor(0)

        self.lotus.blossom.clear()
        self.frame = 0

    def update(self):
        if self.frame < settings.TEST_FRAMES:
            self.lotus.blossom.data = [0,255,0] * settings.LEDS
            for lilypad in self.lotus.lilypads:
                lilypad.setColor(255 << 16)

        elif self.frame < settings.TEST_FRAMES * 2:
            self.lotus.blossom.data = [0,0,255] * settings.LEDS
            for lilypad in self.lotus.lilypads:
                lilypad.setColor(255 << 8)

        elif self.frame < settings.TEST_FRAMES * 3:
            self.lotus.blossom.data = [255,0,0] * settings.LEDS
            for lilypad in self.lotus.lilypads:
                lilypad.setColor(255)

        else:
            self.lotus.changeMode(self.lotus.attract_mode)
            self.lotus.resetLilypads()

        self.frame += 1