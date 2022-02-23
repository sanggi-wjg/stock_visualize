import argparse

from app.exceptions import InvalidCommandArgs
from app.lib.chart.chart_creator import ChartCreator
from app.lib.chart.dataframe_converter import DataFrameConverter
from app.service.stock_price_service import StockPriceService

from app.command.base_command import BaseCommand
from app.service.stock_service import StockService
from app.utils import get_today_date_format


class StockChartCreator(BaseCommand):
    help = 'Create stock chart'

    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    def add_arguments(self):
        self.parser.add_argument('-stock_name', default = '삼성전자', type = str,
                                 choices = [stock.stock_name for stock in self.stock_service.lists()])
        self.parser.add_argument('-start_date', default = '1980-01-01', type = str)
        self.parser.add_argument('-end_date', default = get_today_date_format('%Y-%m-%d'), type = str)
        self.parser.add_argument('-chart_term', default = 10, type = int)

        self.args = self.parser.parse_args()
        if not self.args.start_date or not self.args.end_date:
            # TODO: dateformat 체크하면 좋은데 구찮
            raise InvalidCommandArgs("Invalid date")

    def handle(self, *args, **kwargs):
        chart_creator = ChartCreator(self.args.start_date, self.args.end_date)

        dataframe = DataFrameConverter.stock_price_to_dataframe(
            self.stock_price_service.get_price_list(
                self.args.stock_name, self.args.start_date, self.args.end_date
            )
        )
        chart_creator.create(dataframe)


stock_chart_creator = StockChartCreator(argparse.ArgumentParser())
stock_chart_creator.operate()
