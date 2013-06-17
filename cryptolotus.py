import settings
import random

from twisted.application import service, internet
from twisted.python import log
from twisted.internet import task, reactor
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

from simulator import SimulatorFactory
from lilypad import LilyPad
from blossom import Blossom
from serialwireless import SerialWireless
from modes import BootMode, AttractMode, LoginMode, PlayMode

from profilehooks import timecall

class CryptoLotus(service.Service):

    def __init__(self):
        self.blossom = Blossom(self)
        self.lilypads = []

        for i in range(settings.LILYPADS):
            self.lilypads.append(LilyPad(self, i))

        self.blossom_providers = []
        self.lilypad_providers = []

        # self.normal_modes = []
        # self.normal_modes.append(ColorWheel(0.005))
        # self.normal_modes.append(Paparazzi())

        # # normal modes
        # images = [f for f in listdir(settings.ATTRACT_PATH) if isfile(join(settings.ATTRACT_PATH, f))]

        # for image in images:
        #     self.normal_modes.append(SlitScan(join(settings.ATTRACT_PATH, image), 1))

        # # reward modes
        # self.reward_modes = []
        # images = [f for f in listdir(settings.REWARD_PATH) if isfile(join(settings.REWARD_PATH, f))]

        # for image in images:
        #     self.reward_modes.append(SlitScan(join(settings.REWARD_PATH, image), 1))

        # self.frame = 0
        # self.cycle = 0

        try:
            from ws2801 import WS2801

            self.strips = WS2801()
            self.addBlossomProvider(self.strips)

        except:
            log.msg("Could not initialize WS2801 strips over SPI!")

    
        from twisted.internet.serialport import SerialPort

        self.wireless = SerialWireless()
        self.serial_port = SerialPort(wireless, '/dev/ttyAMA0', reactor, 57600)
        self.addLilypadProvider(self.wireless)


        self.boot_mode = BootMode(self)
        self.attract_mode = AttractMode(self)
        self.login_mode = LoginMode(self)
        self.play_mode = PlayMode(self)

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
        self.blossom.clear()
        self.loop.stop()

application = service.Application("CryptoLotus")

service_collection = service.IServiceCollection(application)
lotus = CryptoLotus()
lotus.setServiceParent(service_collection)

internet.TCPServer(settings.SIMULATOR_PORT, lotus.getSimulatorFactory()).setServiceParent(service_collection)