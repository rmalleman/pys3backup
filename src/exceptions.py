__author__ = 'matt'


class KeyDoesNotExist(Exception):
    __slots__ = ('key',)

    def __init__(self,key):
        self.key = key

    def __str__(self):
        return 'Web Service Unavailable (%s)' % (self.key)
