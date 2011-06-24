import time
from twisted.web import client

from twisted.protocols import basic

class CachingProxyProtocol(basic.LineReceiver):
    def __init__(self, cache):
        self.cache = cache

    def urlFetched(self, data, url, start):
        self.transport.write(data)
        self.transport.loseConnection()
        print 'fetched', url,
        print 'in', time.time() - start

    def storeInCache(self, data, url):
        self.cache[url] = data
        return data

    def lineReceived(self, url):
        if not url.startswith('http://'):
            return
        start = time.time()
        print 'fetching', url
        if url in self.cache:
            data = self.cache[url]
            self.urlFetched(data, url, start)
        else:
            deferredData = client.getPage(url)
            deferredData.addCallback(self.storeInCache, url)
            deferredData.addCallback(self.urlFetched, url, start)

from twisted.internet import protocol
class ProxyFactory(protocol.ServerFactory):
    def __init__(self):
        self.cache = {}
    
    def buildProtocol(self, addr):
        p = CachingProxyProtocol(self.cache)
        return p

from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
factory = ProxyFactory()
endpoint.listen(factory)

reactor.run()
