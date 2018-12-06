import os
from twisted.internet import protocol, reactor

class Echo(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()

PORT = 8000
proxy_port = int(os.environ.get('PORT', PORT))
reactor.listenTCP(proxy_port, EchoFactory())
reactor.run()
