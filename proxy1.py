import time
import urllib2

from twisted.protocols import basic

class ProxyProtocol(basic.LineReceiver):
    def lineReceived(self, url):
        if not url.startswith('http://'):
            return
        start = time.time()
        print 'fetching', url
        connection = urllib2.urlopen(url)
        data = connection.read()
        print 'fetched', url,
        self.transport.write(data)
        self.transport.loseConnection()
        print 'in', time.time() - start

from twisted.internet import protocol
class ProxyFactory(protocol.ServerFactory):
    protocol = ProxyProtocol

from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
factory = ProxyFactory()
endpoint.listen(factory)

reactor.run()
