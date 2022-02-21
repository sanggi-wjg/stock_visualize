import math

import FinanceDataReader as fdr
import argparse

from pandas import Series

from app.command.base_command import BaseCommand
from app.service.market_service import MarketService
from app.service.stock_service import StockService


class StockRegister(BaseCommand):
    help = 'Register Stocks'

    market_service: MarketService = MarketService()
    stock_service: StockService = StockService()
    market_name: str = ""

    def add_arguments(self):
        self.parser.add_argument('-market_name', default = 'kosdaq',
                                 choices = [market.market_name for market in self.market_service.lists()])
        args = self.parser.parse_args()

        self.market_name = args.market_name

    def handle(self, *args, **kwargs):
        datasets = fdr.StockListing(self.market_name)

        for index, data in datasets.iterrows():
            if is_stock_series(data):
                self.create_stock(data)
            else:
                self.print.warning(f"{data['Name']} is not stock")

    def create_stock(self, data: Series):
        if not self.stock_service.is_exist_equal(data['Name']):
            self.stock_service.create(self.market_name, data['Symbol'], data['Name'])
            self.print.info(f"Register {data['Name']}")
        else:
            self.print.warning(f"{data['Name']} is already registered")


def is_stock_series(data: Series) -> bool:
    """
    exclude call option, put option, etf
    """
    if isinstance(data['Sector'], float) and isinstance(data['Industry'], float):
        if math.isnan(data['Sector']) and math.isnan(data['Industry']):
            return False

    return True


stock_register = StockRegister(argparse.ArgumentParser())
stock_register.operate()
