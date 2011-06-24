class Memcached(object):
    def __init__(self, reactor=None):
        if reactor is None:
            from twisted.internet import reactor
        self.reactor = reactor
        self.store = {}
        self.timeouts = {}

    def get(self, key):
        return self.store[key]

    def set(self, key, value, flags, timeout=0):
        self.cancelTimeout(key)
        self.store[key] = (value, flags)
        if timeout > 0:
            timeoutCall = self.reactor.callLater(timeout, self.delete, key)
            self.timeouts[key] = timeoutCall
        return key

    def delete(self, key):
        self.cancelTimeout(key)
        del self.store[key]

    def cancelTimeout(self, key):
        dc = self.timeouts.get(key)
        if dc and dc.active():
            dc.cancel()


