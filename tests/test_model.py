import unittest

from app.database import Market, Index
from app.exceptions import MarketException, IndexException


class ModelTestCase(unittest.TestCase):

    def test_clean_market_entity(self):
        Market("kospi")

        with self.assertRaises(MarketException):
            Market(name = "NotMarketName")

    def test_clean_index_entity(self):
        Index(name = "KS11")

        with self.assertRaises(IndexException):
            Index(name = "NotIndexName")
