import argparse

import FinanceDataReader as fdr
from pandas import DataFrame

from app.command.base_command import BaseCommand
from app.service.stock_price_service import StockPriceService
from app.service.stock_service import StockService


class StockPriceRegister(BaseCommand):
    help = 'Register Stock Prices'

    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    def add_arguments(self):
        self.parser.add_argument('-stock_name', default = '삼성전자', type = str, help = 'Stock name',
                                 choices = [stock.stock_name for stock in self.stock_service.lists()])
        # self.parser.add_argument('-s', '--start', default = '1980-01-01', help = 'Start Date',
        #                          choices = [stock.stock_code for stock in self.stock_service.lists()])
        # self.parser.add_argument('-e', '--end', default = '2099-12-31', help = 'End Date',
        #                          choices = [stock.stock_code for stock in self.stock_service.lists()])

        self.args = self.parser.parse_args()

    def handle(self, *args, **kwargs):
        # get stock
        stock_code = self.stock_service.get_equal_name(self.args.stock_name).stock_code
        self.print.info(f"{self.args.stock_name}({stock_code})")

        # get request stock dataframe
        dataframe: DataFrame = fdr.DataReader(stock_code)
        self.print.warning(dataframe.tail(5))

        # register stock prices
        self.stock_price_service.create_dataframe(dataframe, stock_code)
        self.print.info(f"Done")


register = StockPriceRegister(argparse.ArgumentParser())
register.operate()
