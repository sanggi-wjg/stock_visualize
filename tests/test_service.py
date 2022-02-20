import unittest
from unittest import skip

from app.exceptions import MarketException
from app.service.market_service import MarketService
from app.service.stock_service import StockService


class MarketServiceTestCase(unittest.TestCase):
    market_service: MarketService = MarketService()

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        self.market_service.delete_equal(market_name = "test")
        self.market_service.close()

    def test_create(self):
        # given
        market_name = "test"

        # when
        market = self.market_service.create(market_name)

        # then
        self.assertEqual(market.market_name, market_name.upper())

    def test_create_fail(self):
        # given
        market_name = "NotAllowed"

        # when
        # then
        with self.assertRaises(MarketException):
            self.market_service.create(market_name)

    def test_get_or_create(self):
        # given
        market_name = "test"

        # when
        market = self.market_service.get_or_create(market_name)

        # then
        self.assertEqual(market.market_name, market_name.upper())

    def test_lists(self):
        # given
        # when
        markets = self.market_service.lists()

        # then
        for market in markets:
            self.assertIsInstance(market.id, int)
            self.assertIsInstance(market.market_name, str)

    def test_get_equal(self):
        # given
        market_name = 'kospi'
        self.market_service.get_or_create(market_name)

        # when
        market = self.market_service.get_equal(market_name)

        # then
        self.assertEqual(market.market_name, market_name.upper())


class StockServiceTestCase(unittest.TestCase):
    market_service: MarketService = MarketService()
    stock_service: StockService = StockService()

    def setUp(self) -> None:
        market_name = "test"

        self.market = self.market_service.get_or_create(market_name)

    def tearDown(self) -> None:
        market_name = "test"
        stock_code, stock_name = "1", "삼성"

        self.stock_service.delete_equal(stock_name)
        self.market_service.delete_equal(market_name)
        self.market_service.close()
        self.stock_service.close()

    def test_create(self):
        # given
        stock_code, stock_name = "1", "삼성"

        # when
        stock = self.stock_service.create(self.market, stock_code, stock_name)

        # then
        self.assertEqual(stock.stock_code, stock_code)
        self.assertEqual(stock.stock_name, stock_name)

    def test_is_exist_equal(self):
        # given
        stock_code, stock_name = "1", "삼성"

        # when
        stock = self.stock_service.create(self.market, stock_code, stock_name)

        is_exist = self.stock_service.is_exist_equal(stock_name)
        is_exist2 = self.stock_service.is_exist_equal("삼성2")

        # then
        self.assertEqual(is_exist, True)
        self.assertEqual(is_exist2, False)

    def test_get_equal_name(self):
        # given
        stock_code, stock_name = "1", "삼성"

        # when
        self.stock_service.create(self.market, stock_code, stock_name)

        stock = self.stock_service.get_equal_name(stock_name)

        # then
        self.assertEqual(stock.stock_code, stock_code)
        self.assertEqual(stock.stock_name, stock_name)


class StockPriceServiceTestCase(unittest.TestCase):
    pass
