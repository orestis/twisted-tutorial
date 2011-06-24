import time
from twisted.web import client
from twisted.protocols import basic

from twisted.internet import defer

def getCachedPage(url, cache):
    if url in cache:
        data = cache[url]
        return defer.succeed(data)
    else:
        def _storeInCache(data, url):
            cache[url] = data
            return data
        d = client.getPage(url)
        d.addCallback(_storeInCache, url)
        return d

class CachingProxyProtocol(basic.LineReceiver):
    def __init__(self, cache):
        self.cache = cache

    def lineReceived(self, url):
        if not url.startswith('http://'):
            return
        start = time.time()
        print 'fetching', url
        deferredData = getCachedPage(url, self.cache)
        deferredData.addCallback(self.urlFetched, url, start)

    def urlFetched(self, data, url, start):
        self.transport.write(data)
        self.transport.loseConnection()
        print 'fetched', url,
        print 'in', time.time() - start

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
