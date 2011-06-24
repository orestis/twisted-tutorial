from twisted.protocols import basic
from twisted.internet import defer

class MemcachedGetProtocol(basic.LineReceiver):
    def get(self, key):
        self.key = key
        self.value = None
        self.flags = None
        self.deferred = defer.Deferred()
        self.sendLine('get %s' % self.key)
        return self.deferred

    def lineReceived(self, line):
        if line.startswith('VALUE'):
            _, key, flags, length = line.split()
            self.flags = int(flags)
            self.length = int(length)
            self.buffer = []
            self.setRawMode()
        elif line.startswith('END'):
            self.deferred.callback((self.value, self.flags))
            self.transport.loseConnection()

    def rawDataReceived(self, data):
        self.buffer.append(data)
        raw = ''.join(self.buffer)
        if len(raw) >= self.length + len('\r\n'):
            self.value = raw[:self.length]
            rest = raw[self.length + len('\r\n'):]
            self.setLineMode(rest)

from twisted.internet import protocol
class MemcachedGetFactory(protocol.Factory):
    protocol = MemcachedGetProtocol

if __name__ == '__main__':
    from twisted.internet import reactor, endpoints

    endpoint = endpoints.TCP4ClientEndpoint(reactor, '127.0.0.1', 11211)
    factory = MemcachedGetFactory()
    d = endpoint.connect(factory)
    def got_protocol(p):
        deferredValue = p.get('a')
        def got_v((value, flags)):
            print 'VALUE', value, flags
            reactor.stop()
        deferredValue.addCallback(got_v)
        
    d.addCallback(got_protocol)

    reactor.run()
