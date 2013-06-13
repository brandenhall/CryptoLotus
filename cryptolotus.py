import settings
import random

from twisted.application import service, internet
from twisted.python import log
from twisted.internet import task

from os import listdir
from os.path import isfile, join

from simulator import SimulatorFactory
from lilypad import LilyPad
from blossom import Blossom
from blossom.modes import ColorWheel, Paparazzi, SlitScan

class CryptoLotus(service.Service):

    def __init__(self):
        self.blossom = Blossom(self)
        self.lilypads = []

        for i in range(settings.NUM_LILYPADS):
            self.lilypads.append(LilyPad(self, i))

        self.blossom_providers = []
        self.lilypad_providers = []

        self.normal_modes = []
        self.normal_modes.append(ColorWheel(0.005))
        self.normal_modes.append(Paparazzi())

        # normal modes
        images = [f for f in listdir(settings.ATTRACT_PATH) if isfile(join(settings.ATTRACT_PATH, f))]

        for image in images:
            self.normal_modes.append(SlitScan(join(settings.ATTRACT_PATH, image), 2))

        # reward modes
        self.reward_modes = []
        images = [f for f in listdir(settings.REWARD_PATH) if isfile(join(settings.REWARD_PATH, f))]

        for image in images:
            self.reward_modes.append(SlitScan(join(settings.REWARD_PATH, image), 1))

        self.frame = 0
        self.cycle = 0

        try:
            from ws2801 import WS2801

            self.strips = WS2801()
            self.addBlossomProvider(self.strips)

        except:
            log.msg("Could not initialize WS2801 strips over SPI!")

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

    def onLilypadPress(self, id):
        log.msg("Press lilypad %d" % (id,))

    def onLilypadRelease(self, id):
        log.msg("Release lilypad %d" % (id,))

    def updateLilypad(self, lilypad):
        for provider in self.lilypad_providers:
            provider.updateLilypad(lilypad)

    def update(self):
        
        if self.frame == 0:
            self.cycle = (self.cycle + 1) % settings.REWARD_RATE

            if self.cycle == 0:
                pass
            else:
                # start normal mode
                self.blossom_mode = random.choice(self.normal_modes)

#        if self.frame < 256:
#            fade = 255 - self.frame

#        elif self.frame > settings.SHOW_TIME * settings.FRAME_RATE - 256:
#            fade = 255 - ((settings.SHOW_TIME * settings.FRAME_RATE) - self.frame)

#        else:
#            fade = 0

        self.blossom_mode.draw(self.blossom)

#        self.blossom.data = [max(0, x - fade) for x in self.blossom.data]

        self.blossom.update()

        self.frame += 1
        self.frame %= settings.SHOW_TIME * settings.FRAME_RATE

    def getSimulatorFactory(self):
        f = SimulatorFactory(self, 'ws://0.0.0.0:%d' % (settings.SIMULATOR_PORT,))
        return f
   
    def stopService(self):
        service.Service.stopService(self)
        self.blossom.data = [0,0,0] * 720
        self.blossom.update()
        self.loop.stop()

application = service.Application("CryptoLotus")
service_collection = service.IServiceCollection(application)
lotus = CryptoLotus()
lotus.setServiceParent(service_collection)

internet.TCPServer(settings.SIMULATOR_PORT, lotus.getSimulatorFactory()).setServiceParent(service_collection)
