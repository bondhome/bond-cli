from queue import Queue
from threading import RLock, Thread

KNRM = "\x1B[0m"
KRED = "\x1B[31m"
KBLD = "\x1B[1m"

lock = RLock()

q = Queue()


def console_task():
    while True:
        item = q.get()
        if item is None:
            return
        with lock:
            print(item)


Thread(target=console_task).start()


class LogLine(object):
    def __init__(self, line):
        q.put(line)


class ErrorLine(object):
    def __init__(self, line):
        q.put(KRED + line + KNRM)


class ExceptionLine(object):
    def __init__(self, e):
        q.put(KRED + str(e) + KNRM)


def console_terminate():
    q.put(None)
