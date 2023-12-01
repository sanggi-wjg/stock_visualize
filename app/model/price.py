import math
from dataclasses import dataclass
from decimal import Decimal


@dataclass(order=True, slots=True)
class Price(object):
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    change: Decimal

    def __init__(
        self, open: float, close: float, high: float, low: float, change: float
    ):
        if math.isnan(change):
            change = 0.0

        self.open = Decimal(str(open))
        self.close = Decimal(str(close))
        self.high = Decimal(str(high))
        self.low = Decimal(str(low))
        self.change = Decimal(str(change))
