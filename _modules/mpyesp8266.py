# -*- coding: utf-8 -*-
'''
Provide the module for the MicroPython-specific libraries of a proxy-minion.
'''

from __future__ import absolute_import

# Import python libs
import logging
import salt.utils

log = logging.getLogger(__name__)

__proxyenabled__ = ['mpyesp8266']
__virtualname__ = 'mpyesp8266'


def __virtual__():
    '''
    Only work on systems that are a proxy minion
    '''
    log.debug('mpyesp8266 module __virtual__() called...')
    try:
        if salt.utils.is_proxy() and __opts__['proxy']['proxytype'] == 'mpyesp8266':
            return __virtualname__
    except KeyError:
        return (False, 'The mpyesp8266 execution module failed to load.  Check the proxy key in pillar.')

    return (False, 'The mpyesp8266 execution module failed to load: only works on a micropython_esp8266 proxy minion.')
#

def copy_file(src=None, dst=None):
    return True

#
def check_firmware():
    ret = __proxy__['mpyesp8266.check_firmware']()
    ret2 = ret.split('\x1F')
    import json
    return json.loads(ret2[1])

def toggle_led():
    ret = __proxy__['mpyesp8266.toggle_led']()
    ret2 = ret.split('\x1F')
    import json
    return json.loads(ret2[1])

#
def test():
    ret = __proxy__['mpyesp8266.test']()
    ret2 = ret.split('\x1F')
    import json
    return json.loads(ret2[1])
