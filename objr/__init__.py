# This file is placed in the Public Domain.


"""objects reactor


SYNOPSIS

    >>> from objr import Reactor
    >>> reactor.register("command", command)
    >>> reactor.start()


INSTALL

    $ pip install objr


DESCRIPTION

    OBJR is a threaded, defer exceptions for later, keep on running callback engine.


COPYRIGHT

    OBJR is Public Domain.

"""


from . import errors, reactor, thread


from .errors  import *
from .reactor import *
from .thread  import *


def __dir__():
    return (
        'Errors',
        'errors',
        'later',
        'launch'
        'Reactor',
        'Thread'
    )
