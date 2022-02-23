from typing import List

import pandas as pd
from pandas import DataFrame

from app.database import StockPrice


class DataFrameConverter:

    @classmethod
    def stock_price_to_dataframe(cls, stock_prices: List[StockPrice]) -> DataFrame:
        """

        :param stock_prices:
        :type stock_prices:
        :return: DataFrame
        :rtype: DataFrame
        """
        return pd.DataFrame(
            [price.price_close for price in stock_prices],
            index = [price.date for price in stock_prices],
            columns = ['PRICE']
        )

    @classmethod
    def index_to_dataframe(cls, data) -> DataFrame:
        return NotImplemented
