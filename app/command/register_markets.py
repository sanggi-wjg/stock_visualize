import argparse

from app.command.base_command import BaseCommand
from app.service.market_service import MarketService


class MarketRegister(BaseCommand):
    help = "Register Markets"

    market_service: MarketService = MarketService()
    markets: list = ["kospi", "kosdaq"]

    def add_arguments(self):
        pass

    def handle(self, *args, **kwargs):
        for name in self.markets:
            market = self.market_service.get_or_create(name)
            self.print.info(f"Get or Create Market({market.market_name})")


market_register = MarketRegister(argparse.ArgumentParser())
market_register.operate()
