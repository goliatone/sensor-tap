#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import traceback
import grovepi
import urllib, httplib
import time

from src.control import Loop, Command

#TODO: Reader extend Command
#TODO: Tie Command with URLRequest

class PIRReader(Command):
    """PIRReader"""
    def __init__(self, pin_number=8, interval=5, label="Command"):
        super(Command, self, self.collect, interval, label).__init__()
        self._pin_number = pin_number
        self.value = None
        grovepi.pinMode(pin_number, "INPUT")

    def collect(self):
        try:
            movement = grovepi.digitalRead(self._pin_number)
            self.value = { "m": movement }
        except (IOError,TypeError) as e:
            print "IOError", e
        if self.verbose: print "PIR: ", movement
        return self.value


class DHTReader(Command):
    """DHTReader"""
    def __init__(self, pin_number=7):
        super(Command, self, self.collect, interval, label).__init__()
        self._pin_number = pin_number
        self.value = None
        grovepi.pinMode(pin_number, "INPUT")

    def collect(self):
        try:
            [ temp, hum ] = grovepi.dht(self._pin_number, 1)
            self.value = { "t": temp, "h": hum }
        except (IOError,TypeError) as e:
            print "IOError", e
        if self.verbose: print "DHT: ", self.value
        return self.value

class TapRequest(object):
    """TapRequest"""
    def __init__(self, host='localhost', port='8080'):
        super(TapRequest, self).__init__()
        self._host = host
        self._port = port
        self._endpoint = "%s:%s"%(host, port)
        self.headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}

    def build_params(self):
        self.params = self.build_params()

    def build_request(self):
        self._connection = httplib.HTTPConnection(self._endpoint)

    def execute(self):
        self.build_params()
        self.build_request()
        try:
            self._connection.request('POST', self._endpoint, self.params, self.headers)
            self._connection.close()
        except Exception as e:
            print "Error: ", e


def main():
    parser = argparse.ArgumentParser(description='Sensor Collector controller')
    parser.add_argument('-H', '--host', required=True, help='Host to build HTTP connection URL')
    parser.add_argument('-P', '--port', required=True, help='Port to build HTTP connection URL')
    args = parser.parse_args()

    motion = PIRReader(pin_number=8)
    motionCommand = Command(motion.execute, interval=2, label="Motion Command")

    climate = DHTReader(pin_number=7)
    climateCommand = Command(climate.execute, interval=10, label="Climate Command")

    loop = Loop()
    loop.add_command(motionCommand)
    loop.add_command(climateCommand)
    loop.start()



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

