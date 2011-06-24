class Memcached(object):
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store[key]

    def set(self, key, value, flags, timeout=0):
        self.store[key] = (value, flags)
        return key

    def delete(self, key):
        del self.store[key]

