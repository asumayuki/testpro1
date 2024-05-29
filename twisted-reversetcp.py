from twisted.internet import reactor, protocol

class Proxy(protocol.Protocol):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.buffer = b""
        self.client = None

    def connectionMade(self):
        factory = protocol.ClientFactory()
        factory.protocol = ProxyClient
        factory.proxy = self
        reactor.connectTCP(self.host, self.port, factory)

    def dataReceived(self, data):
        self.buffer += data
        if self.client:
            self.client.write(data)

    def write(self, data):
        self.transport.write(data)

class ProxyClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.proxy.client = self

    def dataReceived(self, data):
        self.factory.proxy.write(data)

    def connectionLost(self, reason):
        self.factory.proxy.transport.loseConnection()

class ProxyFactory(protocol.Factory):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def buildProtocol(self, addr):
        return Proxy(self.host, self.port)

if __name__ == "__main__":
    # Configure reverse proxy settings
    listen_port = 8888
    target_host = "example.com"
    target_port = 80

    # Start the reverse proxy
    reactor.listenTCP(listen_port, ProxyFactory(target_host, target_port))
    print(f"Reverse proxy is listening on port {listen_port} and forwarding to {target_host}:{target_port}")

    # Run the event loop
    reactor.run()
