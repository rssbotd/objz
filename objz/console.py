# This file is placed in the Public Domain.


"console"


from .client  import Client
from .event   import Event


class Console(Client):

    "Console"

    def callback(self, evt):
        "wait for callback."
        Client.callback(self, evt)
        evt.wait()

    def poll(self):
        "poll console and create event."
        evt      = Event()
        evt.txt  = input("> ")
        evt.type = "command"
        return evt

    def raw(self, txt):
        "overload this."
        raise NotImplementedError


def __dir__():
    return (
        'Console',
    )
