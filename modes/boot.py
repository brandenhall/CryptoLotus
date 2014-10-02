import settings

from twisted.python import log

class BootMode:
    
    def __init__(self, lotus):
        self.lotus = lotus
        self.lilypads_ready = False
        self.frame = 0

    def startMode(self):
        for lilypad in self.lotus.lilypads:
            lilypad.setColor(0)

        self.lotus.blossom.clear()
        self.frame = 0

        if self.lotus.wireless is None:
            self.lilypads_ready = True
        else:
            self.lotus.blossom.data = [0,128,128] * settings.LEDS
            self.lotus.resetLilypads()

    def stopMode(self):
        pass

    def update(self):
        if self.lilypads_ready:

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
                self.lotus.changeMode(self.lotus.current_mode)

            self.frame += 1

        else:
            if any(lilypad.active for lilypad in self.lotus.lilypads):
                self.lilypads_ready = True
