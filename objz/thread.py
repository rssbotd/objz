# This file is placed in the Public Domain.
# pylint: disable=R0902,R0903,R0911,W0105,W0718


"threads"


import io
import queue
import threading
import time
import traceback
import types as rtypes


rpr = object.__repr__


"errors"


class Errors:

    "Errors"

    errors = []

    @staticmethod
    def format(exc):
        "format an exception"
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                           )
        for line in stream.readlines():
            res += line + "\n"
        return res


def errors(outer):
    "display errors."
    for exc in Errors.errors:
        outer(Errors.format(exc))


def later(exc):
    "add an exception"
    excp = exc.with_traceback(exc.__traceback__)
    Errors.errors.append(excp)


"threads"


class Thread(threading.Thread):

    "Thread"

    def __init__(self, func, thrname, *args, daemon=True, **kwargs):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._result   = None
        self.name      = thrname or (func and named(func)) or named(self).split(".")[-1]
        self.out       = None
        self.queue     = queue.Queue()
        self.sleep     = None
        self.starttime = time.time()
        if func:
            self.queue.put_nowait((func, args))

    def __iter__(self):
        return self

    def __next__(self):
        yield from dir(self)

    def size(self):
        "return qsize"
        return self.queue.qsize()

    def join(self, timeout=1.0):
        "join this thread."
        super().join(timeout)
        return self._result

    def run(self):
        "run this thread's payload."
        func, args = self.queue.get()
        try:
            self._result = func(*args)
        except Exception as ex:
            time.sleep(1.0)
            later(ex)


def named(obj):
    "return a full qualified name of an object/function/module."
    if isinstance(obj, rtypes.ModuleType):
        return obj.__name__
    typ = type(obj)
    if '__builtins__' in dir(typ):
        return obj.__name__
    if '__self__' in dir(obj):
        return f'{obj.__self__.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj) and '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    if '__class__' in dir(obj):
        return f"{obj.__class__.__module__}.{obj.__class__.__name__}"
    if '__name__' in dir(obj):
        return f'{obj.__class__.__name__}.{obj.__name__}'
    return None


def launch(func, *args, **kwargs):
    "launch a thread."
    nme = kwargs.get("name", named(func))
    thread = Thread(func, nme, *args, **kwargs)
    thread.start()
    return thread


"timer"


class Timer:

    "Timer"

    def __init__(self, sleep, func, *args, thrname=None):
        self.args  = args
        self.func  = func
        self.sleep = sleep
        self.name  = thrname or named(func)
        self.state = {}
        self.timer = None

    def run(self):
        "run the payload in a thread."
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self):
        "start timer."
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.daemon = True
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self):
        "stop timer."
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    "Repeater"

    def run(self):
        launch(self.start)
        super().run()


"interface"


def __dir__():
    return (
        'Errors',
        'Repeater',
        'Thread',
        'Timer',
        'later',
        'errors',
        'launch'
    )
