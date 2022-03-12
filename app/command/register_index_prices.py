import argparse

import FinanceDataReader as fdr
from pandas import DataFrame

from app.command.base_command import BaseCommand
from app.database import Index
from app.service.index_price_service import IndexPriceService
from app.service.index_service import IndexService
from app.utils import get_today_date_format


class IndexPriceRegister(BaseCommand):
    help = 'Register Index Prices (현재 DB에 등록되어 있는 indexes 들에 대해서 Price 를 등록합니다.)'

    index_service: IndexService = IndexService()
    index_price_service: IndexPriceService = IndexPriceService()

    def add_arguments(self):
        self.parser.add_argument('-start_date', default = '1980-01-01', type = str,
                                 help = "Start date")
        self.parser.add_argument('-end_date', default = get_today_date_format('%Y-%m-%d'), type = str,
                                 help = "End date")
        self.parser.add_argument('-index', default = None, type = str, help = '인덱스')

        self.args = self.parser.parse_args()

    def handle(self, *args, **kwargs):
        if self.args.index is not None:
            self.try_register(self.index_service.get_equal_name(self.args.index))
        else:
            for index in self.index_service.lists():
                self.try_register(index)

    def try_register(self, index: Index):
        self.print.info(f"Register {index.index_name}")

        # get index dataframe
        dataframe = fdr.DataReader(index.index_name, self.args.start_date, self.args.end_date)
        # register
        self.index_price_service.create_all_with_dataframe(dataframe, index)


register = IndexPriceRegister(argparse.ArgumentParser())
register.operate()
