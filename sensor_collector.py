#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grovepi
import urllib, httplib
import time
import requests
import json
from collections import OrderedDict
import ConfigParser

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
    if not value: value = get_default_payload()
    try:
        [ temp, hum ] = grovepi.dht(DHT_SENSOR, 1)
        value.update({'t': temp, 'h': hum})
    except (IOError, TypeError) as e:
        print 'DHT IOError: ', e
    return value


def collect_pir(value=None):
    if not value: value = get_default_payload()
    try:
        move = grovepi.digitalRead(PIR_SENSOR)
        value.update({'m': move})
    except (IOError, TypeError) as e:
        print 'PIR IOError: ', e
    return value


def collect_ultrasonic(value=None):
    if not value: value = get_default_payload()
    try:
        sensor = grovepi.ultrasonicRead(SONIC_SENSOR)
        value.update({'u': sensor})
    except (IOError, TypeError) as e:
        print 'PIR IOError: ', e
    return value

def collect_light(value=None):
    if not value: value = get_default_payload()
    try:
        light = grovepi.analogRead(LIGHT_SENSOR)
        value.update({'l': light})
    except (IOError, TypeError) as e:
        print 'LIGHT SENSOR IOError: ', e
    return value


def collect_sound(value=None):
    if not value: value = get_default_payload()
    try:
        sound = grovepi.analogRead(SOUND_SENSOR)
        value.update({'s': sound})
    except (IOError, TypeError) as e:
        print 'SOUND SENSOR IOError: ', e
    return value


def collect_timestamp(value):
    value.update({'timestamp': int(time.time())})
    return value


def get_default_payload():
    return {'uuid': UUID}


def log(msg, params):
    if DEBUG:
        try:
            print msg.format(**params)
        except Exception as e:
            print "LOG Exception: %s" % e


config = ConfigParser.ConfigParser()
config.read('config.ini')

# URI = '/sensor/collect'
# HOST = '192.168.1.145'
# PORT = '3000'
# URL_TEMPLATE = 'http://%s:%s%s'
# UUID = '34add6809dd36514dd43811455cfb596'
URI = config.get('requests', 'uri')
HOST = config.get('requests', 'host')
PORT = config.get('requests', 'port')
URL_TEMPLATE = config.get('requests', 'url_template')

UUID = config.get('auth', 'uuid')

count = 0
value = {}
params = []
DEBUG = True


SOUND_SENSOR = 0 # Analog
LIGHT_SENSOR = 2 # Analog
DHT_SENSOR = 7   # Digital
PIR_SENSOR = 8   # Digital
SONIC_SENSOR = 4 # Digital

grovepi.pinMode(PIR_SENSOR, 'INPUT')


def select_unique(data):
    return [i for n, i in enumerate(data) if i not in data[n + 1:]]


while True:
    try:

        if count % 16 == 0:
            value = collect_dht()
            log('temp = {t} C\thumidity = {h}%', value)

        if count % 32 == 0:
            value = collect_light()
            log('light = {l}', value)

        if count % 2 == 0:
            value = collect_sound(value)
            log('sound= {s}', value)
        # if count % 2 == 0:
            value = collect_pir(value)
            log('movement= {m}', value)
        # if count % 2 == 0:
            value = collect_ultrasonic(value)
            log('ultrasonic= {u}', value)
        # if count % 2 == 0:
            value = collect_timestamp(value)

        if count % 48 == 0 and len(params) != 0:
            params = select_unique(params)
            params = request(params)
        else: params.append(value.copy())

        count += 1
        time.sleep(1)

    except (IOError,TypeError, Exception) as e:
        print 'Error: ', e
