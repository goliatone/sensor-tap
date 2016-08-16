#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import traceback
import time


class Loop(object):
    """docstring for Loop"""
    def __init__(self, interval=1):
        super(Loop, self).__init__()
        self._cmds =[]
        self.reset(interval=interval)

    def add_command(self, cmd):
        self._cmds.append(cmd)

    def reset(self, interval=1):
        self._tick = -1
        self._stopped = False
        self._interval = interval

    def start(self):
        self.reset()
        self._loop()

    def stop(self):
        self._stopped = True

    def _loop(self):
        while not self._stopped:
            self._tick += 1
            for i, cmd in enumerate(self._cmds):
                cmd.tick(self._tick)
            time.sleep(self._interval)


class Command(object):
    """docstring for Command"""
    def __init__(self, func, interval=5, label="Command"):
        super(Command, self).__init__()
        self.func = func
        self._interval = interval
        self.label = label

    def tick(self, count):
        if count % self._interval == 0:
            self.func()


def print_temperature():
    print 'TASK 1: TEMP'

def print_movement():
    print 'TASK 2: MOVEMENT'


cmd1 = Command(print_movement, 2, label="Movement")
cmd2 = Command(print_temperature, 15, label="Temperature")

loop = Loop(1)
loop.add_command(cmd1)
loop.add_command(cmd2)
loop.start()




