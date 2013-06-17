import settings

from twisted.python import log

from blossom.patterns import Paparazzi

class LoginMode:
    
    def __init__(self, lotus):
        self.lotus = lotus
        self.frame = 0
        self.paparazzi = Paparazzi()

    def startMode(self):
        for lilypad in self.lotus.lilypads:
            lilypad.setColor(0)

        self.lotus.blossom.clear()

    def update(self):
        num_active = 0
        for lilypad in self.lotus.lilypads:
            if lilypad.active:
                num_active += 1
                lilypad.setColor(255 << 16 | 255 << 8 | 255)
            else:
                lilypad.setColor(0)

        if num_active > 0:
            self.lotus.blossom.data = self.paparazzi.draw()

        else:
            self.lotus.changeMode(self.lotus.play_mode)