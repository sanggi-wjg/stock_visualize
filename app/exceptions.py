#########################################
# Market Entity Exception
#########################################
class MarketException(Exception):
    pass


class MarketNotFound(MarketException):
    """
    Market not found
    """
    pass


#########################################
# Stock Entity Exception
#########################################
class StockException(Exception):
    pass


class StockNotFound(StockException):
    """
    Stock not found
    """
    pass


#########################################
# StockPrice Entity Exception
#########################################
class StockPriceException(Exception):
    pass


#########################################
# StockPrice Entity Exception
#########################################
class IndexException(Exception):
    pass


#########################################
# Commands Exception
#########################################
class CommandException(Exception):
    pass


class InvalidCommandArgs(CommandException):
    pass


#########################################
# Chart Exception
#########################################
class ChartException(Exception):
    pass


class InvalidConvertOption(ChartException):
    pass
