import json
import sys
import traceback
import lilypad

from autobahn.websocket import WebSocketServerFactory, WebSocketServerProtocol
from twisted.python import log

INIT_EVENT = 'init'


class SimulatorProtocol(WebSocketServerProtocol):

    def __init__(self, factory):
        self.factory = factory

    def onMessage(self, msg, binary):
        try:
            message = json.loads(msg)

            log.msg(message)

            if message['type'] == INIT_EVENT:
                self.factory.lotus.addSimulator(self)

            if message['type'] == lilypad.PRESS_EVENT:
                self.factory.lotus.onLilypadPress(int(message['id']))

            elif message['type'] == lilypad.RELEASE_EVENT:
                self.factory.lotus.onLilypadRelease(int(message['id']))

        except ValueError:
            log.msg('Bad JSON from Simulator')

        except:
            (exc_type, exc_value, exc_traceback) = sys.exc_info()
            #print exception type
            print exc_type
            tb_list = traceback.extract_tb(sys.exc_info()[2])
            tb_list = traceback.format_list(tb_list)
            for elt in tb_list:
                log.msg(elt)

    def updateBlossom(self, blossom):
        message = {}
        message['type'] = 'blossom'
        message['data'] = blossom.data

        self.sendMessage(json.dumps(message))

    def updateLilypad(self, lilypad):
        message = {}
        message['type'] = 'lilypad'
        message['id'] = lilypad.id
        message['color'] = lilypad.color

        self.sendMessage(json.dumps(message))

    def connectionMade(self):
        WebSocketServerProtocol.connectionMade(self)
        log.msg("Simulator connected...")
        self.factory.lotus.addBlossomProvider(self)
        self.factory.lotus.addLilypadProvider(self)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        log.msg("Simulator disconnected...")


class SimulatorFactory(WebSocketServerFactory):

    def __init__(self, lotus, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.lotus = lotus
        self.protocol = SimulatorProtocol
        self.setProtocolOptions(allowHixie76=True)

    def buildProtocol(self, addr):
        return SimulatorProtocol(self)
