class MarketException(Exception):
    pass


class MarketNotFound(MarketException):
    pass


class StockException(Exception):
    pass


class StockNotFound(StockException):
    pass
