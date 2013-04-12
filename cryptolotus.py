import settings

from twisted.application import service, internet
from twisted.python import log
from twisted.internet import reactor
from twisted.internet import task

from simulator import SimulatorFactory
from lilypad import LilyPad
from blossom import Blossom

NUM_LILYPADS = 6

def makeColor(r, g, b):
    return r << 16 | g << 8 | b

def colorWheel(pos):
    if pos < 85:
        return makeColor(pos * 3, 255 - pos * 3, 0)

    elif pos < 170:
        pos -= 85
        return makeColor(255 - pos * 3, 0, pos *3)

    else:
        pos -= 170
        return makeColor(0, pos * 3, 255 - pos * 3)

class CryptoLotus(service.Service):

    def __init__(self):
        self.blossom = Blossom(self)
        self.lilypads = []

        for i in range(NUM_LILYPADS):
            self.lilypads.append(LilyPad(self, i + 1))

        self.blossom_providers = []
        self.lilypad_providers = []
        self.music_providers = []

        self.loop_index = 0
        self.loop = task.LoopingCall(self.drawRainbow)
        



    def addSimulator(self, simulator):
        self.blossom.update()
        self.loop.start(1.0/30.0)

    def addLilypadProvider(self, provider):
        self.lilypad_providers.append(provider)

    def addBlossomProvider(self, provider):
        self.blossom_providers.append(provider)

    def addMusicProvider(self, provider):
        self.music_providers.append(provider)  

    def updateBlossom(self, blossom):
        for provider in self.blossom_providers:
            provider.updateBlossom(blossom)

    def drawRainbow(self):
        for i in range(2160):
            self.blossom[i] = colorWheel(((i * 256 / 256) + self.loop_index) % 256)

        self.loop_index +=1
        self.blossom.update()


    def getSimulatorFactory(self):
        f = SimulatorFactory(self, 'ws://0.0.0.0:%d' % (settings.SIMULATOR_PORT,))
        return f

application = service.Application("CryptoLotus")
serviceCollection = service.IServiceCollection(application)
service = CryptoLotus()

internet.TCPServer(settings.SIMULATOR_PORT, service.getSimulatorFactory()).setServiceParent(serviceCollection)