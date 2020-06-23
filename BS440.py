from __future__ import print_function
import sys
import pygatt.backends
import logging
from ConfigParser import SafeConfigParser
import time
import subprocess
from struct import *
from binascii import hexlify
import os

# Interesting characteristics
Char_weight = '00008a21-0000-1000-8000-00805f9b34fb'  # weight data
Char_command = '00008a81-0000-1000-8000-00805f9b34fb'  # command register

'''
The decode functions Read Medisana BS440 Scale hex Indication and 
decodes scale values from hex data string.
Each function receives the hex handle and bytevalues and
return a dictionary with the decoded data
'''

def sanitize_timestamp(timestamp):
    retTS = time.time()
    return retTS

def decodeWeight(handle, values):
    '''
    decodeWeight
    Handle: 0x1b
    Byte[0] = 0x1d
    Returns:
        valid (True, False)
        weight (5,0 .. 180,0 kg)
        timestamp (unix timestamp date and time of measurement)
        person (1..9)
        note: in python 2.7 to force results to be floats,
        devide by float.
        '''
    data = unpack('<BHxxIxxxxB', bytes(values[0:14]))
    retDict = {}
    retDict["valid"] = (data[0] == 0x1d)
    retDict["weight"] = data[1]/100.0
    retDict["timestamp"] = sanitize_timestamp(data[2])
    retDict["person"] = data[3]
    return retDict

def processIndication(handle, values):
    '''
    Indication handler:
    Receives indication and stores values into result Dict
    (see decode functions for Dict definition)
    handle: byte
    value: bytearray
    '''
    if handle == handle_weight:
        result = decodeWeight(handle, values)
        if result not in weightdata:
            log.info(str(result))
            weightdata.append(result)
        else:
            log.info('Duplicate weightdata record')
    else:
        log.debug('Unhandled Indication encountered')

def wait_for_device(devname):
    global adapter
    found = False
    while not found:
        try:
            # wait for scale to wake up and connect to it
            found = adapter.filtered_scan(devname)
        except pygatt.exceptions.BLEError:
            # reset adapter when (see issue #33)
            adapter.reset()
    return

def connect_device(address):
    device_connected = False
    tries = 3
    device = None
    while not device_connected and tries > 0:
        try:
            device = adapter.connect(address, 8, addresstype)
            device_connected = True
        except pygatt.exceptions.NotConnectedError:
            tries -= 1
    return device

def init_ble_mode():
    global log
    p = subprocess.Popen("sudo btmgmt le on", stdout=subprocess.PIPE,
                         shell=True)
    (output, err) = p.communicate()
    if not err:
        log.info(output)
        return True
    else:
        log.info(err)
        return False

'''
Main program loop
'''

config = SafeConfigParser()
config.read('BS440.ini')
path = "plugins/"
plugins = {}

# set up logging
numeric_level = getattr(logging,
                        config.get('Program', 'loglevel').upper(),
                        None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level,
                    format='%(asctime)s %(levelname)-8s %(funcName)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=config.get('Program', 'logfile'),
                    filemode='w')
log = logging.getLogger(__name__)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(numeric_level)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(funcName)s %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)

# Load configured plugins

if config.has_option('Program', 'plugins'):
    config_plugins = config.get('Program', 'plugins').split(',')
    config_plugins = [plugin.strip(' ') for plugin in config_plugins]
    log.info('Configured plugins: %s' % ', '.join(config_plugins))

    sys.path.insert(0, path)
    for plugin in config_plugins:
        log.info('Loading plugin: %s' % plugin)
        mod = __import__(plugin)
        plugins[plugin] = mod.Plugin()
    log.info('All plugins loaded.')
else:
    log.info('No plugins configured.')
sys.path.pop(0)

ble_address = config.get('Scale', 'ble_address')
device_name = config.get('Scale', 'device_name')
device_model = config.get('Scale', 'device_model')

if device_model == 'BS410':
    addresstype = pygatt.BLEAddressType.public
    # On BS410 time=0 equals 1/1/2010. 
    # time_offset is used to convert to unix standard
    time_offset = 1262304000
else:
    addresstype = pygatt.BLEAddressType.random
    time_offset = 0
    
'''
Start BLE comms and run that forever
'''
log.info('BS440 Started')
if not init_ble_mode():
    sys.exit()

adapter = pygatt.backends.GATTToolBackend()
adapter.start()

while True:
    wait_for_device(device_name)
    device = connect_device(ble_address)
    if device:
        weightdata = []
        
        handle_weight = device.get_handle(Char_weight)
        handle_command = device.get_handle(Char_command)
        continue_comms = True

        '''
        subscribe to characteristics and have processIndication
        process the data received.
        '''
        try:
            device.subscribe(Char_weight,
                             callback=processIndication,
                             indication=True)
        except pygatt.exceptions.NotConnectedError:
            continue_comms = False

        '''
        Send the unix timestamp in little endian order preceded by 02 as
        bytearray to handle 0x23. This will resync the scale's RTC.
        While waiting for a response notification, which will never
        arrive, the scale will emit 30 Indications on 0x1b and 0x1e each.
        '''
        if continue_comms:
            timestamp = bytearray(pack('<I', int(time.time() - time_offset)))
            timestamp.insert(0, 2)
            try:
                device.char_write_handle(handle_command, timestamp,
                                         wait_for_response=True)
            except pygatt.exceptions.NotificationTimeout:
                pass
            except pygatt.exceptions.NotConnectedError:
                continue_comms = False
            if continue_comms:
                log.info('Waiting for notifications for another 3 seconds')
                time.sleep(3)
                try:
                    device.disconnect()
                except pygatt.exceptions.NotConnectedError:
                    log.info('Could not disconnect...')

                log.info('Done receiving data from scale')
                # process data if all received well
                if weightdata:
                    # Sort scale output by timestamp to retrieve most recent three results
                    weightdatasorted = sorted(weightdata, key=lambda k: k['timestamp'], reverse=False)
                    
                    # Run all plugins found
                    for plugin in plugins.values():
                        plugin.execute(config, weightdatasorted)
                else:
                    log.error('Continue-conn...')
