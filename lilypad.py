SET_COLOR = "color"
FADE_COLOR = "fade"
SHOW_PATTERN = "pattern"

PRESS_EVENT = "press"
RELEASE_EVENT = "release"

class LilyPad:
    def __init__(self, lotus, id):
        self.lotus = lotus
        self.id = id
        self.active = False

    def setColor(self, color):
        self.lotus.updateLilypad(self.id, SET_COLOR, [color])

    def fadeToColor(self, color, duration, easing=0):
        self.lotus.updateLilypad(self.id, FADE_COLOR, [color, duration, easing])

