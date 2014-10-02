import settings

from twisted.application import service, internet
from twisted.python import log
from twisted.internet import task, reactor

from simulator import SimulatorFactory
from lilypad import LilyPad
from blossom import Blossom
from serialwireless import SerialWireless
from modes import BootMode, GeyserMode
from twisted.internet.serialport import SerialPort


class CryptoLotus(service.Service):

    def setup(self):

        self.blossom = Blossom(self)
        self.lilypads = []

        for i in range(settings.LILYPADS):
            self.lilypads.append(LilyPad(self, i))

        self.blossom_providers = []
        self.lilypad_providers = []

        try:
            from ws2801 import WS2801

            self.strips = WS2801()
            self.addBlossomProvider(self.strips)

        except:
            log.msg("Could not initialize WS2801 strips over SPI!")

        self.wireless = None
        self.serial_port = None

        self.wireless = SerialWireless(self)
        self.serial_port = SerialPort(self.wireless, settings.SERIAL_PORT, reactor, settings.SERIAL_BAUD)
        self.addLilypadProvider(self.wireless)

        self.boot_mode = BootMode(self)
        self.geyser_mode = GeyserMode(self)

        self.current_mode = self.geyser_mode

        self.mode = self.boot_mode
        self.mode.startMode()

        self.loop_index = 0
        self.loop = task.LoopingCall(self.update)
        self.loop.start(1.0/settings.FRAME_RATE)

    def addSimulator(self, simulator):
        pass

    def addLilypadProvider(self, provider):
        self.lilypad_providers.append(provider)

    def addBlossomProvider(self, provider):
        self.blossom_providers.append(provider)

    def updateBlossom(self, blossom):
        for provider in self.blossom_providers:
            provider.updateBlossom(blossom)

    def updateLilypad(self, lilypad):
        for provider in self.lilypad_providers:
            provider.updateLilypad(lilypad)

    def resetLilypads(self):
        for provider in self.lilypad_providers:
            provider.resetLilypads()

    def changeMode(self, mode):
        self.mode = mode
        self.mode.startMode()

    def update(self):
        self.mode.update()
        self.blossom.update()

    def getSimulatorFactory(self):
        f = SimulatorFactory(self, 'ws://0.0.0.0:%d' % (settings.SIMULATOR_PORT,))
        return f

    def stopService(self):
        service.Service.stopService(self)
        self.mode.stopMode()
        self.blossom.clear()
        self.loop.stop()

application = service.Application("CryptoLotus")

service_collection = service.IServiceCollection(application)

lotus = CryptoLotus()
lotus.setServiceParent(service_collection)

internet.TCPServer(settings.SIMULATOR_PORT, lotus.getSimulatorFactory()).setServiceParent(service_collection)

lotus.setup()
