from twisted.protocols.basic import LineReceiver
from twisted.python import log


class SerialWireless(LineReceiver):

    def connectionMade(self):
        log.msg('Serial port connected.')


    def lineReceived(self, line):
        log.msg('Got serial ', line)

    def reset(self):
        self.transport.write(0)

    def updateLilypad(self, lilypad):
        red = lilypad.color >> 16 & 0xFF
        green = lilypad.color >> 8 & 0xFF
        blue = lilypad.color & 0xFF
        self.transport.write([1, lilypad.id, red, green, blue])

        log.msg("HOLLA! ", lilypad.id, lilypad.color)
