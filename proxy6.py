import time
from twisted.web import client
from twisted.protocols import basic

def getMemcachedPage(url, memcacheClient, timeout=0):
    d = memcacheClient.get(url)
    def got((v, f)):
        if v is not None:
            return v
        else:
            d = client.getPage(url)
            def _storeInCache(data, url):
                d = memcacheClient.set(url, data, 0, timeout)
                d.addCallback(lambda _: data)
                return d
            d.addCallback(_storeInCache, url)
            return d
    d.addCallback(got)
    return d

class CachingProxyProtocol(basic.LineReceiver):
    def __init__(self, cache):
        self.cache = cache

    def lineReceived(self, url):
        if not url.startswith('http://'):
            return
        start = time.time()
        print 'fetching', url
        deferredData = getMemcachedPage(url, self.cache)
        deferredData.addCallback(self.urlFetched, url, start)

    def urlFetched(self, data, url, start):
        self.transport.write(data)
        self.transport.loseConnection()
        print 'fetched', url,
        print 'in', time.time() - start

from twisted.internet import protocol
from memcached_client5 import MemcachedClient
class ProxyFactory(protocol.ServerFactory):
    def __init__(self):
        self.cache = MemcachedClient(
            endpoints.TCP4ClientEndpoint(reactor, '127.0.0.1', 11211))
    
    def buildProtocol(self, addr):
        p = CachingProxyProtocol(self.cache)
        return p

from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ServerEndpoint(reactor, 8000)
factory = ProxyFactory()
endpoint.listen(factory)

reactor.run()
