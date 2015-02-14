import grovepi
# from grove_rgb_lcd import *
import urllib, httplib
import time
import requests
import json
from collections import OrderedDict


##This should be there now
# Connect the DHt sensor to port 7
dht_sensor_port = 7

# Connect to PIR sensor, port 8
pir_sensor = 8
grovepi.pinMode(pir_sensor, 'INPUT')

URI = '/sensor/collect'
HOST = '192.168.1.145'
PORT = '3000'
URL_TEMPLATE = 'http://%s:%s%s'


def request(payload):
    if not payload: return []

    url = URL_TEMPLATE % (HOST, PORT, URI)
    headers = {'content-type': 'application/json'}

    try:
        requests.post(url, data=json.dumps(payload), headers=headers)
    except Exception as e:
        print 'Error: ', e

    return []


def collect_dht(value=None):
    if not value: value = {}
    try:
        [ temp, hum ] = grovepi.dht(dht_sensor_port, 1)
        value.update({'t':temp, 'h': hum})
    except (IOError, TypeError) as e:
        print 'DHT IOError: ', e
    return value


def collect_pir(value=None):
    if not value: value = {}
    try:
        move = grovepi.digitalRead(pir_sensor)
        value.update({'m': move})
    except (IOError, TypeError) as e:
        print 'PIR IOError: ', e
    return value


def collect_timestamp(value):
    value.update({'timestamp': int(time.time())})
    return value


def log(msg, params):
    if DEBUG:
        print msg.format(**params)


count = 0
value = {}
params = []
DEBUG = True


while True:
    try:

        if count % 16 == 0:
            value = collect_dht()
            log('temp = {t} C\thumidity = {h}%', value)

        if count % 2 == 0:
            value = collect_pir(value)
            log('movement= {m}', value)

        if count % 2 == 0:
            value = collect_timestamp(value)
            # log('timestamp= {timestamp}', value)

        if count % 32 == 0 and len(params) != 0:
            params = [i for n, i in enumerate(params) if i not in params[n + 1:]]
            print params
            params = request(params)
        else: params.append(value.copy())

        count += 1
        time.sleep(1)

    except (IOError,TypeError) as e:
        print 'Error: ', e
