from typing import List
from unittest import skip

import FinanceDataReader as fdr

import unittest

from pandas import DataFrame, Series

from app.database import StockPrice
from app.exceptions import InvalidConvertOption
from app.lib.chart.chart_utils import plt_colors, DataFrameConverter, financial_crises
from app.service.stock_price_service import StockPriceService
from app.service.stock_service import StockService
from app.vo import Price


class FdrTestCase(unittest.TestCase):
    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    @skip(reason = "just test")
    def test_get_spec_stock(self):
        stock_code = "005930"
        df: DataFrame = fdr.DataReader(stock_code, start = "2022-02-01")
        # print(df.tail(20))

        self.stock_price_service.create_all_with_dataframe(df, stock_code)

    def test_get_index(self):
        kospi = fdr.DataReader("KS11", "2022-01-01")
        print(kospi)


class ChartUtilsTestCase(unittest.TestCase):

    def test_plt_colors(self):
        color = plt_colors(0)

        self.assertIsInstance(color, str)
        self.assertEqual(plt_colors(0), 'blue')
        self.assertEqual(plt_colors(5), 'yellow')
        self.assertEqual(plt_colors(6), 'blue')

    def get_mock_stock_prices(self):
        return [
            StockPrice(0, Price(open = 100, close = 100, high = 100, low = 100, change = 0.1), '2022-01-01'),
            StockPrice(0, Price(open = 100, close = 200, high = 100, low = 100, change = 0.1), '2022-01-02'),
            StockPrice(0, Price(open = 100, close = 300, high = 100, low = 100, change = 0.1), '2022-01-03'),
        ]

    def test_dataframe_converter(self):
        # given
        stock_prices = self.get_mock_stock_prices()

        # when
        dataset = DataFrameConverter.stock_price_to_dataframe(stock_prices)

        # then
        self.assertIsInstance(dataset, DataFrame)

        self.assertEqual(dataset.loc['2022-01-01']['Price'], 100)
        self.assertEqual(dataset.loc['2022-01-02']['Price'], 200)
        self.assertEqual(dataset.loc['2022-01-03']['Price'], 300)

    def test_dataframe_convert_raise(self):
        # given
        stock_prices = self.get_mock_stock_prices()

        # when
        # then
        with self.assertRaises(InvalidConvertOption):
            DataFrameConverter.stock_price_to_dataframe(stock_prices, standardization = True, normalization = True)

    def test_dataframe_convert_standardization(self):
        # given
        stock_prices = self.get_mock_stock_prices()

        # when
        dataset = DataFrameConverter.stock_price_to_dataframe(stock_prices, standardization = True)

        # then
        self.assertIsInstance(dataset, Series)
        self.assertEqual(dataset['2022-01-01'], -1.0)
        self.assertEqual(dataset['2022-01-02'], 0.0)
        self.assertEqual(dataset['2022-01-03'], 1.0)

    def test_dataframe_convert_normalization(self):
        # given
        stock_prices = self.get_mock_stock_prices()

        # when
        dataset = DataFrameConverter.stock_price_to_dataframe(stock_prices, normalization = True)

        # then
        self.assertIsInstance(dataset, Series)

    def test_financial_crises(self):
        crises = financial_crises()

        self.assertIsInstance(crises, List)
        for crisis in crises:
            self.assertIsInstance(crisis[0], str)
            self.assertIsInstance(crisis[1], str)
            self.assertIsInstance(crisis[2], str)
