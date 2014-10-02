from twisted.protocols.basic import LineReceiver
from twisted.python import log

import time


class SerialWireless(LineReceiver):

    def __init__(self, lotus):
        self.lotus = lotus

    def connectionMade(self):
        log.msg('Serial port connected.')


    def lineReceived(self, line):
        log.msg("SERIAL", line)

        id = int(line[0])
        active = line[1] == '1'

        log.msg("Lilypad #", id, active)

        self.lotus.lilypads[id].active = active

    def resetLilypads(self):
        self.transport.write(self.reset_code)

    def updateLilypad(self, lilypad):
        log.msg("Set lilypad color", lilypad.id, lilypad.color)

        red = chr(lilypad.color >> 16 & 0xFF)
        green = chr(lilypad.color >> 8 & 0xFF)
        blue = chr(lilypad.color & 0xFF)
        self.transport.write(chr(1) + chr(lilypad.id) + red + green + blue);
