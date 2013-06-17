from twisted.protocols.basic import LineReceiver
from twisted.python import log


class SerialWireless(LineReceiver):

    def connectionMade(self):
        log.msg('Serial port connected.')


    def lineReceived(self, line):
        log.msg('Got serial ', line)

    def resetLilypads(self):
        self.transport.write(bin(0)]

    def updateLilypad(self, lilypad):
        red = lilypad.color >> 16 & 0xFF
        green = lilypad.color >> 8 & 0xFF
        blue = lilypad.color & 0xFF
        self.transport.write(bin(1))
        self.transport.write(bin(lilypad.id))
        self.transport.write(bin(red))
        self.transport.write(bin(green))
        self.transport.write(bin(blue))
