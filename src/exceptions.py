__author__ = 'matt'


class KeyDoesNotExist(Exception):
    __slots__ = ('key',)

    def __init__(self,key):
        self.key = key

    def __str__(self):
        return 'File does not exist on the S3 bucket (%s)' % (self.key)
