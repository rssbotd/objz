# This file is placed in the Public Domain.
# pylint: disable=W0613,W0718

"client"


from objr.reactor import Reactor
from objt.errors  import later
from objx.broker  import Broker
from objx.object  import Object


from .command import Commands
from .parser   import parse


class Client(Reactor):

    "Client"

    cache = Object()

    def __init__(self):
        Reactor.__init__(self)
        Broker.register(self)
        self.register("command", command)

    def display(self, evt):
        for text in evt.result:
            self.say(evt.channel, text)

    def dosay(self, channel, txt):
        "make say."
        self.raw(txt)

    def say(self, channel, txt):
        "echo on verbose."
        self.raw(txt)

    def raw(self, txt):
        "print to screen."
        raise NotImplementedError


def command(bot, evt):
    "check for and run a command."
    parse(evt)
    func = Commands.cmds.get(evt.cmd, None)
    if func:
        try:
            func(evt)
        except Exception as ex:
            later(ex)
    if "ready" in dir(evt):
        bot.display(evt)
        evt.ready()


def __dir__():
    return (
       'Client',
    )
