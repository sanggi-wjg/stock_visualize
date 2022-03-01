import argparse
from typing import List, Tuple

from pandas import DataFrame

from app.exceptions import InvalidCommandArgs, StockNotFound, IndexNotFound
from app.lib.chart.chart_creator import create_chart
from app.lib.chart.chart_utils import DataFrameConverter
from app.service.index_price_service import IndexPriceService
from app.service.index_service import IndexService
from app.service.stock_price_service import StockPriceService

from app.command.base_command import BaseCommand
from app.service.stock_service import StockService
from app.utils import get_today_date_format


class ChartCreator(BaseCommand):
    help = 'Create chart (그래프 차트 그리기)'

    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    index_service: IndexService = IndexService()
    index_price_service: IndexPriceService = IndexPriceService()

    def add_arguments(self):
        # date
        self.parser.add_argument('-start_date', default = '1980-01-01', type = str,
                                 help = "Start date")
        self.parser.add_argument('-end_date', default = get_today_date_format('%Y-%m-%d'), type = str,
                                 help = "End date")

        # Manipulate data
        self.parser.add_argument('-s', '--standard', default = False, type = bool,
                                 help = '표준화')
        self.parser.add_argument('-n', '--normal', default = False, type = bool,
                                 help = '정규화')
        self.parser.add_argument('-e', '--earning', default = False, type = bool,
                                 help = '수익률')

        # term, implement not yet
        self.parser.add_argument('-chart_term', default = 10, type = int,
                                 help = "(!미구현) chart 여러개 그린다고 하면 사용하자")

        # indexes, stocks
        self.parser.add_argument('-t', '--targets', nargs = '+', required = True,
                                 help = 'Stock names + Index names')
        """
        (-t NHN 카카오 NAVER)
        (-t NHN KS11 -e True -start_date=2014-01-01 )
        """

        self.args = self.parser.parse_args()

        if not self.args.start_date or not self.args.end_date:
            raise InvalidCommandArgs("Invalid argument: date")  # dateformat 체크 구찮
        if not self.args.targets:
            raise InvalidCommandArgs("Invalid argument: targets")

    def handle(self, *args, **kwargs):
        stock_targets, index_targets = self.clean_args_targets()
        dataframe = self.convert_entities_to_dataframes(stock_targets, index_targets)
        create_chart(dataframe, stock_targets + index_targets)

    def clean_args_targets(self) -> Tuple[List[str], List[str]]:
        """
        :return: arguments 로 입력 받은 targets 를 현재 DB 조회 후 있는 것만 append 해서 return list
        """
        stock_targets, index_targets = [], []

        for target in self.args.targets:
            # stock
            try:
                stock = self.stock_service.get_equal_name(target)
            except StockNotFound:
                pass
            else:
                stock_targets.append(stock.stock_name)
                continue
            # index
            try:
                index = self.index_service.get_equal_name(target)
            except IndexNotFound:
                pass
            else:
                index_targets.append(index.index_name)

        self.print.warning("Clean targets", stock_targets, index_targets)
        return stock_targets, index_targets

    def convert_entities_to_dataframes(self, stock_targets: List[str], index_targets: List[str]) -> List[DataFrame]:
        """
        :param stock_targets stock name
        :param index_targets index name
        :return: stock_price entities 를 List[DataFrame] 으로 converting
        """
        dfs = [
            DataFrameConverter.stock_price_to_dataframe(
                self.stock_price_service.get_price_list(stock_name, self.args.start_date, self.args.end_date),
                standardization = self.args.standard,
                normalization = self.args.normal,
                earning_ratio = self.args.earning
            )
            for stock_name in stock_targets
        ]
        dfs.extend([
            DataFrameConverter.index_price_to_dataframe(
                self.index_price_service.get_price_list(index_name, self.args.start_date, self.args.end_date),
                standardization = self.args.standard,
                normalization = self.args.normal,
                earning_ratio = self.args.earning
            )
            for index_name in index_targets
        ])
        return dfs


creator = ChartCreator(argparse.ArgumentParser())
creator.operate()
