from twisted.internet import protocol, defer
from memcached_client2 import MemcachedGetProtocol
from memcached_client3 import MemcachedSetProtocol

getFactory = protocol.Factory()
getFactory.protocol = MemcachedGetProtocol

setFactory = protocol.Factory()
setFactory.protocol = MemcachedSetProtocol

class MemcachedClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get(self, key):
        deferredValue = defer.Deferred()
        d = self.endpoint.connect(getFactory)
        def got_protocol(p):
            d2 = p.get(key)
            def got_response(r):
                deferredValue.callback(r)
            d2.addCallback(got_response)
        d.addCallback(got_protocol)
        return deferredValue

    def set(self, key, value, flags, timeout=0):
        deferredValue = defer.Deferred()
        d = self.endpoint.connect(setFactory)
        def got_protocol(p):
            d2 = p.set(key, value, flags, timeout)
            def got_response(r):
                deferredValue.callback(r)
            d2.addCallback(got_response)
        d.addCallback(got_protocol)
        return deferredValue

if __name__ == '__main__':

    from twisted.internet import reactor, endpoints
    endpoint = endpoints.TCP4ClientEndpoint(reactor, '127.0.0.1', 11211)

    client = MemcachedClient(endpoint)
    d = client.set('a', 'asdf', 0)
    def set(_):
        print 'SET'
        reactor.stop()

    d.addCallback(set)
    reactor.run()





