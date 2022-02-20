import unittest
from unittest import skip

from app.service.market_service import MarketService, StockService


class MarketServiceTestCase(unittest.TestCase):
    market_service: MarketService = MarketService()

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_create(self):
        market_name = "test"
        self.market_service.create(market_name)
        self.market_service.delete_equal(market_name)

    def test_delete(self):
        market_name = "test"
        self.market_service.get_or_create(market_name)

        market_name = "test"
        self.market_service.delete_equal(market_name)


class StockServiceTestCase(unittest.TestCase):
    market_service: MarketService = MarketService()
    stock_service: StockService = StockService()

    def test_create(self):
        # given
        market_name = "test"
        stock_code, stock_name = "1", "삼성"

        # when
        self.stock_service.create(market_name, stock_code, stock_name)

        # then
        self.stock_service.delete_equal(stock_name)
        self.market_service.delete_equal(market_name)
