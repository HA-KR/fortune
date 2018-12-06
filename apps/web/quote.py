# -*- coding: UTF-8 -*-
from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol
import os
import random

class QuoteProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numConnections += 1

    def dataReceived(self, data):
        msg = "[Online: {}]\t>Your Fortune {}: {}".format(self.factory.numConnections, data, self.getQuote())
        self.transport.write(msg.encode('utf-8'))

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote()


class QuoteFactory(Factory):
    numConnections = 0
    def __init__(self, quote=None):
        self.quotes = []
        print("Initing Quotes..")
        with open(os.path.join(os.path.dirname(__file__),"resources/fortunes")) as fo:
            self.quotes  = [q for q in fo.read().split("\n%\n") if len(q.strip()) > 0]
        print("Loaded {} quotes".format(len(self.quotes)))

    def quote(self):
        secure_random = random.SystemRandom()
        q = secure_random.choice(self.quotes) or "An apple a day keeps the doctor away"
        return q

    def buildProtocol(self, addr):
        return QuoteProtocol(self)


PORT = 8000
proxy_port = int(os.environ.get('PORT', PORT))
reactor.listenTCP(proxy_port, QuoteFactory())
reactor.run()
