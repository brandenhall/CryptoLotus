class LilyPad:
    def __init__(self, lotus, id):
        self.lotus = lotus
        self.id = id
        self.active = False
        self.color = 0

    def setColor(self, color):
        self.color = color
        self.lotus.updateLilypad(self)
