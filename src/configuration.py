__author__ = 'matt'

import os
import logging
import exceptions

from ConfigParser import SafeConfigParser, ParsingError

__config = None
log = logging.getLogger(__name__)
fh = logging.FileHandler('/var/tmp/pys3log.txt')
log.addHandler(fh)
CONFIG_FILE = os.path.expanduser('~/.pyS3Backup')
def load(filename=CONFIG_FILE):

    global __config

    if (not os.path.exists(filename) or not os.path.isfile(filename)):
        log.error('[ERROR] %s configuration file does not exist!\n' % (filename))
        return

    __config = SafeConfigParser()

    try:
        __config.read(filename)
        log.info('[INFO] %s configuration file was loaded.\n' % (filename))
    except ParsingError, msg:
        log.error('[ERROR] %s\n' % (msg))
        raise msg

def get():
    global __config
    if (__config is None):
        load()
    return __config


def reset():
    global __config
    __config = None
