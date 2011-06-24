from twisted.internet import protocol

class HelloWorldProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print data

class HelloWorldFactory(protocol.ServerFactory):
    protocol = HelloWorldProtocol


from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
factory = HelloWorldFactory()
endpoint.listen(factory)

reactor.run()
