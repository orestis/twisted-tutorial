from twisted.internet import protocol
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
        d = self.endpoint.connect(getFactory)
        def got_protocol(p):
            return p.get(key)
        d.addCallback(got_protocol)
        return d

    def set(self, key, value, flags, timeout=0):
        d = self.endpoint.connect(setFactory)
        def got_protocol(p):
            return p.set(key, value, flags, timeout)
        d.addCallback(got_protocol)
        return d

if __name__ == '__main__':
    from twisted.internet import reactor, endpoints
    endpoint = endpoints.TCP4ClientEndpoint(reactor, '127.0.0.1', 11211)
    client = MemcachedClient(endpoint)
    d = client.get('a')
    def got_value(r):
        print 'GOT', r
        reactor.stop()

    d.addCallback(got_value)
    reactor.run()







