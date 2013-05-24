import settings

from twisted.application import service, internet
from twisted.python import log
from twisted.internet import task

from simulator import SimulatorFactory
from lilypad import LilyPad
from blossom import Blossom
from blossom.modes import ColorWheel, Paparazzi, SlitScan

NUM_LILYPADS = 6
FRAME_RATE = 30.0


class CryptoLotus(service.Service):

    def __init__(self):
        self.blossom = Blossom(self)
        self.lilypads = []

        for i in range(NUM_LILYPADS):
            self.lilypads.append(LilyPad(self, i))

        self.blossom_providers = []
        self.lilypad_providers = []

        self.blossom_mode = SlitScan('assets/attract/ant-lotusrainwave.jpg', -1)

        try:
            from ws2801 import WS2801

            self.strips = WS2801()
            self.addBlossomProvider(self.strips)

        except:
            log.msg("Could not initialize WS2801 strips over SPI!")

        self.loop_index = 0
        self.loop = task.LoopingCall(self.update)
        self.loop.start(1.0/FRAME_RATE)

    def addSimulator(self, simulator):
        pass

    def addLilypadProvider(self, provider):
        self.lilypad_providers.append(provider)

    def addBlossomProvider(self, provider):
        self.blossom_providers.append(provider)

    def updateBlossom(self, blossom):
        for provider in self.blossom_providers:
            provider.updateBlossom(blossom)

    def onLilypadPress(self, id):
        log.msg("Press lilypad %d" % (id,))

    def onLilypadRelease(self, id):
        log.msg("Release lilypad %d" % (id,))

    def updateLilypad(self, lilypad):
        for provider in self.lilypad_providers:
            provider.updateLilypad(lilypad)

    def update(self):
        self.blossom_mode.draw(self.blossom)
        self.blossom.update()

    def getSimulatorFactory(self):
        f = SimulatorFactory(self, 'ws://0.0.0.0:%d' % (settings.SIMULATOR_PORT,))
        return f

application = service.Application("CryptoLotus")
serviceCollection = service.IServiceCollection(application)
service = CryptoLotus()

internet.TCPServer(settings.SIMULATOR_PORT, service.getSimulatorFactory()).setServiceParent(serviceCollection)
