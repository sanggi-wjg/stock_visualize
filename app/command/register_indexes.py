import argparse

from app.command.base_command import BaseCommand
from app.constants import ALLOW_INDEXES
from app.service.index_service import IndexService


class IndexRegister(BaseCommand):
    help = 'Register Indexes'

    index_service: IndexService = IndexService()

    def add_arguments(self):
        pass

    def handle(self, *args, **kwargs):
        for name in ALLOW_INDEXES:
            index = self.index_service.get_or_create(name)
            self.print.info(f"Get or Create Index({index.index_name})")


register = IndexRegister(argparse.ArgumentParser())
register.operate()
