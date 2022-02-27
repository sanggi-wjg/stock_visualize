import unittest
from unittest import skip

from app.constants import ALLOW_INDEXES
from app.database import StockPrice, Market, Stock, Index, IndexPrice
from app.exceptions import MarketException
from app.service.index_price_service import IndexPriceService
from app.service.index_service import IndexService
from app.service.market_service import MarketService
from app.service.stock_price_service import StockPriceService
from app.service.stock_service import StockService
from app.vo import Price


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
        market = self.market_service.create(Market(market_name))

        # then
        self.assertEqual(market.market_name, market_name.upper())

    def test_create_fail(self):
        # given
        market_name = "NotAllowed"

        # when
        # then
        with self.assertRaises(MarketException):
            self.market_service.create(Market(market_name))

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
        stock = self.stock_service.create(Stock(self.market.id, stock_code, stock_name))

        # then
        self.assertEqual(stock.stock_code, stock_code)
        self.assertEqual(stock.stock_name, stock_name)

    def test_is_exist_equal(self):
        # given
        stock_code, stock_name = "1", "삼성"

        # when
        stock = self.stock_service.create(Stock(self.market.id, stock_code, stock_name))

        is_exist = self.stock_service.is_exist_equal(stock_name)
        is_exist2 = self.stock_service.is_exist_equal("삼성2")

        # then
        self.assertEqual(is_exist, True)
        self.assertEqual(is_exist2, False)

    def test_get_equal_name(self):
        # given
        stock_code, stock_name = "1", "삼성"

        # when
        self.stock_service.create(Stock(self.market.id, stock_code, stock_name))

        stock = self.stock_service.get_equal_name(stock_name)

        # then
        self.assertEqual(stock.stock_code, stock_code)
        self.assertEqual(stock.stock_name, stock_name)

    def test_reverse_relation(self):
        stock = self.stock_service.get_equal_name("삼성전자")

        for price in stock.stock_prices:
            self.assertIsInstance(price, StockPrice)


class StockPriceServiceTestCase(unittest.TestCase):
    market_service: MarketService = MarketService()
    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    def setUp(self) -> None:
        market_name = "test"
        stock_code = "1"
        stock_name = "TestStock"

        market = self.market_service.get_or_create(market_name)
        self.stock_service.delete_equal(stock_name)

        self.stock = self.stock_service.create(Stock(market.id, stock_code, stock_name))

    def tearDown(self) -> None:
        market_name = "test"
        stock_code = "1"
        stock_name = "TestStock"

        self.stock_price_service.delete_equal_stock(stock_name)
        self.stock_service.delete_equal(stock_name)
        self.market_service.delete_equal(market_name)

        self.market_service.close()
        self.stock_service.close()
        self.stock_price_service.close()

    @skip(reason = "only local")
    def test_create(self):
        # given
        date = "2022-02-21"
        price = Price(100.0, 150.0, 200.0, 50.0, 0.001234)

        # when
        stock_price = self.stock_price_service.create(
            StockPrice(self.stock.id, price, date)
        )

        # then
        self.assertEqual(price.open, stock_price.price_open)
        self.assertEqual(price.close, stock_price.price_close)
        self.assertEqual(price.high, stock_price.price_high)
        self.assertEqual(price.low, stock_price.price_low)
        self.assertEqual(price.change, stock_price.price_change)


class StockPriceServiceTestCase2(unittest.TestCase):
    stock_service: StockService = StockService()
    stock_price_service: StockPriceService = StockPriceService()

    def test_get_price_list(self):
        stock_prices = self.stock_price_service.lists("삼성전자", "2022-01-01", "2022-02-01")
        # for stock_price in stock_prices:
            # print(stock_price)


class IndexServiceTestCase(unittest.TestCase):
    index_service: IndexService = IndexService(test_mode = True)

    def test_create(self):
        # given
        index = Index(name = "KS11")

        # when
        index = self.index_service.create(index)

        # then
        self.assertEqual(index.index_name, "KS11")

    def test_get_or_create(self):
        # given
        # when
        # then
        for name in ALLOW_INDEXES:
            self.index_service.get_or_create(name)


class IndexPriceServiceTestCase(unittest.TestCase):
    index_service: IndexService = IndexService(test_mode = True)
    index_price_service: IndexPriceService = IndexPriceService(test_mode = True)

    def test_create(self):
        # given
        index = Index(name = "KS11")
        index = self.index_service.create(index)

        # when
        index_price = IndexPrice(index.id, Price(100.0, 150.0, 200.0, 50.0, 0.001234), '2022-02-01')
        index_price = self.index_price_service.create(index_price)

        # then
        # print(index)
        # print(index_price)
