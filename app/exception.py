class MarketException(Exception):
    pass


class MarketNotFound(MarketException):
    pass


class StockException(Exception):
    pass


class StockNotFound(StockException):
    pass


class StockPriceException(StockException):
    pass


class IndexException(Exception):
    pass


class IndexNotFound(IndexException):
    pass


class IndexPriceException(IndexException):
    pass


class CommandException(Exception):
    pass


class InvalidCommandArgs(CommandException):
    pass


class ChartException(Exception):
    pass


class InvalidConvertOption(ChartException):
    pass
