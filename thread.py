import threading

class TaskThread(threading.Thread):
    """Thread that executes a task every N seconds"""

    def __init__(self, task, times=-1):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 15.0
        self._count = 0
        self._times = times
        self._command = task

    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        while 1:
            if self._finished.isSet(): return

            self._count += 1

            if self._times == self._count:
                return self.shutdown()
            self.task()

            # sleep for interval or until shutdown
            self._finished.wait(self._interval)

    def task(self):
        """The task done by this thread - override in subclasses"""
        self._command()


def print_hello():
    print 'TASK 1: TEMP'

def print_movement():
    print 'TASK 2: MOVEMENT'


task = TaskThread(print_hello, 5)
task.run()

move = TaskThread(print_movement, 5)
move.setInterval(2)
move.run()