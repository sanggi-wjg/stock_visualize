import argparse

import FinanceDataReader as fdr
from pandas import DataFrame

from app.command.base_command import BaseCommand
from app.exceptions import StockNotFound
from app.repository.stock_price_service import StockPriceService
from app.repository.stock_service import StockService


class StockPriceRegister(BaseCommand):
    help = "Register Stock Prices"

    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    def add_arguments(self):
        self.parser.add_argument(
            "-t",
            "--targets",
            nargs="+",
            help="Stock names (-t NHN 카카오 삼성전자)",
            required=True,
        )
        # self.parser.add_argument('-stock_name', default = '삼성전자', type = str, help = 'Stock name',
        #                          choices = [stock.stock_name for stock in self.stock_service.lists()])

        self.args = self.parser.parse_args()

    def handle(self, *args, **kwargs):
        for stock_name in self.args.targets:
            self.try_register(stock_name)

    def try_register(self, stock_name: str):
        try:
            stock = self.stock_service.get_equal_name(stock_name)
            self.print.info(f"{stock.stock_name}({stock.stock_code})")

            # get request stock dataframe
            dataframe: DataFrame = fdr.DataReader(stock.stock_code)
            # self.print.warning(dataframe.tail(5))

            # register stock prices
            self.stock_price_service.create_all_with_dataframe(
                dataframe, stock.stock_code
            )
            self.print.info("Done")

        except StockNotFound as e:
            self.print.error(e)


register = StockPriceRegister(argparse.ArgumentParser())
register.operate()
