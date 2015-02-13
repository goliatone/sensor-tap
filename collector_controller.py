#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import traceback
import grovepi
import urllib, httplib
import time


class PIRReader(object):
    """PIRReader"""
    def __init__(self, pin_number=8):
        super(PIRReader, self).__init__()
        self._pin_number = pin_number
        grovepi.pinMode(pin_number, "INPUT")
        self.value = None

    def collect(self):
        self.value = grovepi.digitalRead(self._pin_number)
        if self.verbose: print "MOVEMENT: ", self.value
        return self.value




##This should be there now
# Connect the DHt sensor to port 7
dht_sensor_port = 7

# Connect to PIR sensor, port 8
pir_sensor = 8
grovepi.pinMode(pir_sensor, "INPUT")

while True:
    try:
        #Get the temperature and Humidity from the DHT sensor
        [ temp, hum ] = grovepi.dht(dht_sensor_port, 1)
        print "temp =", temp, "C\thumadity =", hum,"%"
        #get movement
        move = grovepi.digitalRead(pir_sensor)
        print "movement=", move
        params = urllib.urlencode({'t': temp, 'h': hum, 'm': move,  'token':'YD4U41EMAHIGRLPE'})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("192.168.1.145:3000")
        try:
            conn.request('POST', '/sensor/collect', params, headers)
            # response = conn.getresponse()
            # print response.status
            # data = response.read()
            conn.close()
            time.sleep(16)
        except Exception as e:
            print "Error: ", e

    except (IOError,TypeError) as e:
        print "Error", e



def main():
    parser = argparse.ArgumentParser(description='Sensor Collector controller')
    parser.add_argument('-H', '--host', required=True, help='Host to build HTTP connection URL')
    parser.add_argument('-P', '--port', required=True, help='Port to build HTTP connection URL')
    args = parser.parse_args()

    print args.foo,
    if args.bar:
        print args.bar

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e:
        raise e
    except SystemExit, e:
        raise e
    except Exception, e:
        print str(e)
        traceback.print_exc()
        sys.exit(1)
