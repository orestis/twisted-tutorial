import time
from twisted.web import client

from twisted.protocols import basic

class ProxyProtocol(basic.LineReceiver):

    def urlFetched(self, data, url, start):
        self.transport.write(data)
        self.transport.loseConnection()
        print 'fetched', url,
        print 'in', time.time() - start

    def lineReceived(self, url):
        if not url.startswith('http://'):
            return
        start = time.time()
        print 'fetching', url
        deferredData = client.getPage(url)
        deferredData.addCallback(self.urlFetched, url, start)

from twisted.internet import protocol
class ProxyFactory(protocol.ServerFactory):
    protocol = ProxyProtocol

from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
factory = ProxyFactory()
endpoint.listen(factory)

reactor.run()
