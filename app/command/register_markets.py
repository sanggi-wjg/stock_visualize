import argparse

from app.command.base_command import BaseCommand
from app.constant import ALLOW_MARKETS
from app.repository.market_repository import MarketRepository


class MarketRegister(BaseCommand):
    help = "Register Markets"
    market_repository: MarketRepository = MarketRepository()

    def add_arguments(self):
        pass

    def handle(self, *args, **kwargs):
        market_names: list = [p.lower() for p in ALLOW_MARKETS]

        for name in market_names:
            market = self.market_repository.get_or_create(name)
            self.print.info(f"Get or Create Market({market.market_name})")


market_register = MarketRegister(argparse.ArgumentParser())
market_register.operate()
