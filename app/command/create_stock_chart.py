import argparse
from typing import List

from pandas import DataFrame

from app.exceptions import InvalidCommandArgs, StockNotFound
from app.lib.chart.chart_creator import create_chart
from app.lib.chart.chart_utils import DataFrameConverter
from app.service.stock_price_service import StockPriceService

from app.command.base_command import BaseCommand
from app.service.stock_service import StockService
from app.utils import get_today_date_format


class StockChartCreator(BaseCommand):
    help = 'Create stock chart'

    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    def add_arguments(self):
        self.parser.add_argument('-start_date', default = '1980-01-01', type = str,
                                 help = "Start date")
        self.parser.add_argument('-end_date', default = get_today_date_format('%Y-%m-%d'), type = str,
                                 help = "End date")
        self.parser.add_argument('-chart_term', default = 10, type = int,
                                 help = "미구현 chart 여러개 그린다고 하면 사용하자")

        self.parser.add_argument('-targets', nargs = '+', type = list, required = True)

        self.args = self.parser.parse_args()
        # self.args.targets = ['삼성전자', 'NAVER']

        if not self.args.start_date or not self.args.end_date:
            raise InvalidCommandArgs("Invalid argument: date")  # dateformat 체크 구찮
        if not self.args.targets:
            raise InvalidCommandArgs("Invalid argument: targets")

    def handle(self, *args, **kwargs):
        stock_names = self.clean_args_targets()
        create_chart(
            self.get_stock_dataframes(stock_names), stock_names
        )

    def clean_args_targets(self) -> List[str]:
        """
        :return: arguments 로 입력 받은 targets 를 현재 DB 조회 후 있는 것만 append 해서 return list
        """
        stock_names = []

        for target in self.args.targets:
            try:
                stock = self.stock_service.get_equal_name(target)
            except StockNotFound:
                pass  # future Index get_equal_name
            else:
                stock_names.append(stock.stock_name)

        self.print.warning("Clean targets", stock_names)
        return stock_names

    def get_stock_dataframes(self, stock_names: List[str]) -> List[DataFrame]:
        """
        :param stock_names stock names
        :return: stock_price entities 를 List[DataFrame] 으로 converting
        """
        return [
            DataFrameConverter.stock_price_to_dataframe(
                self.stock_price_service.get_price_list(
                    stock_name, self.args.start_date, self.args.end_date))
            for stock_name in stock_names
        ]


stock_chart_creator = StockChartCreator(argparse.ArgumentParser())
stock_chart_creator.operate()
