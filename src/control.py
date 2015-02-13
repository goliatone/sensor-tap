# -*- coding: utf-8 -*-
import time


class Loop(object):
    """Loop"""
    def __init__(self, interval=1):
        super(Loop, self).__init__()
        self.reset(interval=interval)

    def add_command(self, cmd):
        self._cmds.append(cmd)

    def reset(self, interval=1):
        self._tick = 0
        self._cmds =[]
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
            for cmd in self._cmds:
                cmd.tick(self._tick)
            time.sleep(self._interval)


class Command(object):
    """Command"""
    def __init__(self, func, interval=5):
        super(Command, self).__init__()
        self.func = func
        self._interval = interval

    def tick(self, count):
        if count % self._interval == 0:
            self.func()
