# -*- coding: utf-8 -*-
'''
This is a proxy minion that connects to a ESP8266 running micropython firmware.
'''
from __future__ import absolute_import

# Import python libs
import logging

# Import 3rd-party libs
try:
    HAS_PYBOARD = True
    # wraps pyboard with
    import pyboard
except ImportError:
    HAS_PYBOARD = False

__proxyenabled__ = ['mpyesp8266']
__virtualname__ = 'mpyesp8266'


GRAINS_CACHE = {}
DETAILS = {}


log = logging.getLogger(__file__)

#
def __virtual__():
#    '''
#    Only return if all the modules are available
#    '''
    log.info('>>>mpyesp8266 proxy __virtual__() called...')
    if not HAS_PYBOARD:
        return False, 'Missing dependency pyboard github.com/micropython > tools/pyboard.py'

    return __virtualname__

def init(opts=None):
    '''
    Initialize the library and enter micropythons raw-REPL mode (takes bytes, doesn't echo back).
    '''
    log.info('mpyesp8266 proxy init() called...')
    #get option connection string
    #DETAILS['device'] = opts['proxy'].get('device')
    #log.info('mpyesp8266 proxy DETAILS: ', ', '.join(DETAILS))
    #try to connect
    try:
        DETAILS['pyboard'] = pyboard.Pyboard('/dev/ttyUSB0')
        DETAILS['connected'] = True
        DETAILS['pyboard'].enter_raw_repl()
    except pyboard.PyboardError:
        try:
            DETAILS['pyboard'] = pyboard.Pyboard('/dev/ttyUSB1')
            DETAILS['connected'] = True
            DETAILS['pyboard'].enter_raw_repl()
        except:
            DETAILS['connected'] = False
    except:
        DETAILS['connected'] = False
    #todo wrap
    #if successful
    # do whatever
    #else return false
    #
    DETAILS['initialized'] = True

def initialized():
    return DETAILS.get('initialized', False)

#
def ping():
    return DETAILS['connected']
#def ping():
#    '''
#    Required.
#    Ping the device on the other end of the connection
#    .. code-block: bash
#        salt '*' nxos.cmd ping
#    '''
#    if _worker_name() not in DETAILS:
#        init()
#    try:
#        return DETAILS[_worker_name()].conn.isalive()
#    except TerminalException as e:
#        log.error(e)
#        return False
#
#
def shutdown(opts):
    '''
    Required.
    Disconnect from the board.
    '''
    DETAILS['pyboard'].exit_raw_repl()
    return True
#def shutdown(opts):
#    '''
#    Required.
#    Disconnect
#    '''
#    pass
#    #DETAILS[_worker_name()].close_connection()


def grains():
    '''
    Get the grains from the proxy device.
    '''
    if not GRAINS_CACHE:
        return _grains() #maybe use connection settings here?
    return GRAINS_CACHE


def grains_refresh():
    '''
    Refresh the grains from the proxy device.
    '''
    GRAINS_CACHE = {}
    return grains()

#def _grains(host, protocol=None, port=None):
def _grains():
    '''
    Helper function to the grains from the proxied device.
    '''
    execstring = (
        "import esp, os, sys, machine, network, ubinascii, json\r\n"
        "\r\n"
        "ret = {{}}\r\n"
        "\r\n"
        "ret['fw'] = sys.implementation.name + '_' + sys.platform\r\n"
        "ret['fw_family'] = sys.implementation.name\r\n"
        "ret['fw_platform'] = sys.platform\r\n"
        "ret['fwmajorrelease'] = sys.implementation.version[0]\r\n"
        "ret['fwrelease'] = '.'.join(map(str, sys.implementation.version))\r\n"
        "ret['fwrelease_info'] = sys.implementation.version\r\n"
        "\r\n"
        "if network.WLAN(network.STA_IF).active() or network.WLAN(network.AP_IF).active():\r\n"
        "    ret['ip4_interfaces'] = {{}}\r\n"
        "    ret['ipv4'] = {{}}\r\n"
        "\r\n"
        "if network.WLAN(network.STA_IF).active() and network.WLAN(network.STA_IF).ifconfig()[0] is not '0.0.0.0':\r\n"
        "    ret['ip4_interfaces']['sta'] = network.WLAN(network.STA_IF).ifconfig()[0]\r\n"
        "    ret['ipv4']['sta'] = network.WLAN(network.STA_IF).ifconfig()[0]\r\n"
        "\r\n"
        "if network.WLAN(network.AP_IF).active() and network.WLAN(network.AP_IF).ifconfig()[0] is not '0.0.0.0':\r\n"
        "    ret['ip4_interfaces']['ap'] = network.WLAN(network.AP_IF).ifconfig()[0]\r\n"
        "    ret['ipv4']['ap'] = network.WLAN(network.AP_IF).ifconfig()[0]\r\n"
        "\r\n"
        "ret['machine_id'] = ubinascii.hexlify(machine.unique_id()).decode('utf-8')\r\n"
        "ret['mem_total'] = esp.flash_size()\r\n"
        "ret['flash_id'] = esp.flash_id()\r\n"
        "ret['freq'] = machine.freq()\r\n"
        "\r\n"
        "has_hostname = False\r\n"
        "try:\r\n"
        "    with open('/etc/hostname', 'r') as f:\r\n"
        "        firstline = f.readline().strip()\r\n"
        "        has_hostname = True\r\n"
        "except:\r\n"
        "    pass\r\n"
        "\r\n"
        "try:\r\n"
        "    with open('/hostname', 'r') as f:\r\n"
        "        firstline = f.readline().strip()\r\n"
        "        has_hostname = True\r\n"
        "except:\r\n"
        "    pass\r\n"
        "\r\n"
        "if has_hostname:\r\n"
        "    ret['host'] = firstline\r\n"
        "    ret['nodename'] = firstline\r\n"
        "    ret['id'] = firstline\r\n"
        "    ret['fqdn'] = firstline\r\n"
        "\r\n"
        "ret['pythonversion'] = sys.version_info\r\n"
        "ret['serialnumber'] = ubinascii.hexlify(machine.unique_id()).decode('utf-8')\r\n"
        "ret['virtual'] = 'physical'\r\n"
        "ret['cpu_model'] = 'Xtensa lx106'\r\n"
        "\r\n"
        "ret['hwaddr_interfaces'] = {{}}\r\n"
        "addr = ubinascii.hexlify(network.WLAN(network.STA_IF).config('mac')).decode('utf-8')\r\n"
        "ret['hwaddr_interfaces']['sta'] = ':'.join(addr[i:i+2] for i in range(0,len(addr),2))\r\n"
        "addr = None\r\n"
        "\r\n"
        "addr = ubinascii.hexlify(network.WLAN(network.AP_IF).config('mac')).decode('utf-8')\r\n"
        "ret['hwaddr_interfaces']['ap'] = ':'.join(addr[i:i+2] for i in range(0,len(addr),2))\r\n"
        "\r\n"
        "print('{som}' + json.dumps(ret) + '{eom}')\r\n"
    ).format(som='\x1F', eom='\x1F')
    ret = DETAILS['pyboard'].exec_(execstring)
    ret2 = ret.split('\x1F')
    import json
    mydict = json.loads(ret2[1])
    GRAINS_CACHE.update(mydict)
    return GRAINS_CACHE
#

def check_firmware():
    execstring = ("import esp, ubinascii, ujson\r\n"
        "ret = {{}}\r\n"
        "ret['check_fw'] = esp.check_fw()\r\n"
        "print('{som}' + ujson.dumps(ret) + '{eom}')").format(som='\x1F', eom='\x1F')
    ret = DETAILS['pyboard'].exec_(execstring)
    return ret

def toggle_led():
    execstring = ("import machine, ubinascii, ujson\r\n"
        "led = machine.Pin(0, machine.Pin.OUT)\r\n"
        "ret = {{}}\r\n"
        "led.value( not led.value() )\r\n"
        "ret['toggle_led'] = True\r\n"
        "print('{som}' + ujson.dumps(ret) + '{eom}')").format(som='\x1F', eom='\x1F')
    ret = DETAILS['pyboard'].exec_(execstring)
    return ret
#

