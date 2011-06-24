from twisted.protocols import basic

class MemcachedServerProtocol(basic.LineReceiver):
    def __init__(self, store):
        self.store = store

    def lineReceived(self, line):
        if line.startswith('get'):
            _, key = line.split()
            self.handle_get(key)

        elif line.startswith('set'):
            _, key, flags, timeout, length = line.split()
            self.handle_set(key, int(flags), int(timeout), int(length))

    def handle_get(self, key):
        try:
            value, flags = self.store.get(key)
            self.sendLine('VALUE %s %d %d' % (key, flags, len(value)))
            self.transport.write(value)
            self.sendLine('')
        except KeyError:
            pass
        finally:
            self.sendLine('END')

    def handle_set(self, key, flags, timeout, length):
        self.buffer = []
        self.key = key
        self.flags = flags
        self.timeout = timeout
        self.length = length
        self.setRawMode()
        
    def rawDataReceived(self, data):
        self.buffer.append(data)
        raw = ''.join(self.buffer)
        if len(raw) >= self.length + len('\r\n'):
            value = raw[:self.length]
            rest = raw[self.length + len('\r\n'):]
            self.store.set(self.key, value, self.flags, self.timeout)
            self.sendLine('STORED')
            self.setLineMode(rest)



from memcached1 import Memcached
from twisted.internet import protocol

class MemcachedServerFactory(protocol.ServerFactory):
    def __init__(self):
        self.store = Memcached()

    def buildProtocol(self, addr):
        p = MemcachedServerProtocol(self.store)
        return p

from twisted.internet import reactor, endpoints

endpoint = endpoints.TCP4ServerEndpoint(reactor, 11211)
factory = MemcachedServerFactory()
endpoint.listen(factory)

reactor.run()
