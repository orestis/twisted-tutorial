from twisted.internet import protocol
from memcached_client2 import MemcachedGetProtocol
from memcached_client3 import MemcachedSetProtocol

class MemcachedClient(object):
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def get(self, key):
        factory = protocol.Factory()
        factory.protocol = MemcachedGetProtocol
        d = self.endpoint.connect(factory)
        def got_protocol(p):
            return p.get(key)
        d.addCallback(got_protocol)
        return d

    def set(self, key, value, flags, timeout=0):
        factory = protocol.Factory()
        factory.protocol = MemcachedSetProtocol
        d = self.endpoint.connect(factory)
        def got_protocol(p):
            return p.set(key, value, flags, timeout)
        d.addCallback(got_protocol)
        return d



