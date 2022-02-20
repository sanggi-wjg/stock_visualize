from argparse import Namespace, ArgumentParser
from collections import namedtuple

from app.colorful import green, yellow, red


class BaseCommand:

    def __init__(self, parser: ArgumentParser):
        self.print = namedtuple('CommandPrint', ['info', 'warning', 'error'])
        self.print.info = green
        self.print.warning = yellow
        self.print.error = red
        # self.print.info(f"Command input : {args}")

        # self.args = args
        self.parser = parser

    def operate(self):
        self.add_arguments()
        self.handle()

    def add_arguments(self):
        raise NotImplementedError("add_arguments must declared")

    def handle(self, *args, **kwargs):
        raise NotImplementedError("operate must declared")
