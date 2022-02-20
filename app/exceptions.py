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
#
#########################################
class StockPriceException(Exception):
    pass
