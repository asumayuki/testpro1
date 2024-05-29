from twisted.internet import reactor, ssl
from twisted.internet.protocol import Factory, Protocol

class ProxyClient(Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.clientConnectionMade(self)

    def dataReceived(self, data):
        self.factory.clientDataReceived(data)

class ProxyClientFactory(Factory):
    def __init__(self, server):
        self.server = server
        self.client = None

    def buildProtocol(self, addr):
        return ProxyClient(self)

    def clientConnectionMade(self, client):
        self.client = client
        self.server.transport.resumeProducing()

    def clientDataReceived(self, data):
        self.server.transport.write(data)

class ProxyServer(Protocol):
    def connectionMade(self):
        self.factory.connections.append(self)
        self.clientFactory = ProxyClientFactory(self)
        reactor.connectSSL("destination_host", 443, self.clientFactory, ssl.ClientContextFactory())

    def dataReceived(self, data):
        if self.clientFactory.client:
            self.clientFactory.client.transport.write(data)

    def connectionLost(self, reason):
        self.factory.connections.remove(self)

class ProxyServerFactory(Factory):
    def __init__(self):
        self.connections = []

    def buildProtocol(self, addr):
        return ProxyServer()

if __name__ == "__main__":
    factory = ProxyServerFactory()
    reactor.listenSSL(8443, factory, ssl.DefaultOpenSSLContextFactory('server.key', 'server.crt'))
    reactor.run()
