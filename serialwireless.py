from twisted.protocols.basic import LineReceiver
from twisted.python import log


class SerialWireless(LineReceiver):

    def connectionMade(self):
        log.msg('Serial port connected.')


    def lineReceived(self, line):
        log.msg('Got serial ', line)

    def resetLilypads(self):
        self.transport.write(chr(0))

    def updateLilypad(self, lilypad):
        red = chr(lilypad.color >> 16 & 0xFF)
        green = chr(lilypad.color >> 8 & 0xFF)
        blue = chr(lilypad.color & 0xFF)
        self.transport.write(chr(1) + chr(lilypad.id) + red + green + blue);
