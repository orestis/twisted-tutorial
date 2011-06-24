from twisted.protocols import basic
from twisted.internet import defer

class MemcachedSetProtocol(basic.LineReceiver):
    def set(self, key, value, flags, timeout=0):
        self.deferred = defer.Deferred()
        length = len(value)
        self.sendLine('set %s %d %d %d' % (key, flags, timeout, length))
        self.transport.write(value)
        self.sendLine('')
        return self.deferred

    def lineReceived(self, line):
        if line == 'STORED':
            self.deferred.callback(None)


if __name__ == '__main__':
    from twisted.internet import reactor, endpoints, protocol

    endpoint = endpoints.TCP4ClientEndpoint(reactor, '127.0.0.1', 11211)
    factory = protocol.Factory()
    factory.protocol = MemcachedSetProtocol
    d = endpoint.connect(factory)
    def got_protocol(p):
        deferredValue = p.set('a', '123', 12, 0)
        def set_v(_):
            print 'STORED'
            reactor.stop()
        deferredValue.addCallback(set_v)
        
    d.addCallback(got_protocol)

    reactor.run()
