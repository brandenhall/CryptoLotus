import settings

from twisted.python import log

class PlayMode:
    
    def __init__(self, lotus):
        self.lotus = lotus
        self.frame = 0

    def startMode(self):
        for lilypad in self.lotus.lilypads:
            lilypad.setColor(0)

        self.lotus.blossom.clear()
        self.frame = 0

    def stopMode(self):
        pass

    def update(self):
        pass