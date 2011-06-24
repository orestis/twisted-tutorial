from twisted.protocols import basic

class MemcachedGetProtocol(basic.LineReceiver):
    def get(self, key):
        self.key = key
        self.value = None
        self.flags = None
        self.sendLine('get %s' % self.key)

    def lineReceived(self, line):
        if line.startswith('VALUE'):
            _, key, flags, length = line.split()
            self.flags = int(flags)
            self.length = int(length)
            self.buffer = []
            self.setRawMode()
        elif line.startswith('END'):
            print 'GOT VALUE', self.value, self.flags
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

from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ClientEndpoint(reactor, '127.0.0.1', 11211)
factory = MemcachedGetFactory()
d = endpoint.connect(factory)
def got_protocol(p):
    p.get('a')
d.addCallback(got_protocol)

reactor.run()
