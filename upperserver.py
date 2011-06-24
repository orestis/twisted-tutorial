from twisted.internet import protocol

class UpperProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print data
        self.transport.write(data.upper())

class UpperFactory(protocol.ServerFactory):
    protocol = UpperProtocol


from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
factory = UpperFactory()
endpoint.listen(factory)

reactor.run()
