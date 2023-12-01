from argparse import ArgumentParser, Namespace
from collections import namedtuple

from app.util import magenta, green, yellow, red


class BaseCommand:
    help: str = ""
    args: Namespace = None

    def __init__(self, parser: ArgumentParser):
        self.print = namedtuple("CommandPrint", ["debug", "info", "warning", "error"])
        self.print.debug = magenta
        self.print.info = green
        self.print.warning = yellow
        self.print.error = red
        # self.print.info(f"Command input : {args}")

        # self.args = args
        self.parser = parser
        self.setup()

    def setup(self):
        pass

    def operate(self):
        self.print.info(f"START Command: {self.help or None}")
        self.add_arguments()
        self.handle()
        self.print.info("FINISH Command")

    def add_arguments(self):
        raise NotImplementedError("add_arguments must declared")

    def handle(self, *args, **kwargs):
        raise NotImplementedError("operate must declared")
