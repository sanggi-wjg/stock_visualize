import FinanceDataReader as fdr

import unittest

from pandas import DataFrame

from app.service.stock_price_service import StockPriceService
from app.service.stock_service import StockService


class FdrTestCase(unittest.TestCase):
    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    def test_get_spec_stock(self):
        stock_code = "005930"
        df: DataFrame = fdr.DataReader(stock_code, start = "2022-02-01")
        # print(df.tail(20))

        self.stock_price_service.create_dataframe(df)
