from decimal import Decimal
from typing import List, Tuple

import pandas as pd
from matplotlib import dates
from matplotlib.dates import DateFormatter, YearLocator, MonthLocator
from pandas import DataFrame

from app.database import StockPrice, IndexPrice
from app.exceptions import InvalidConvertOption


def financial_crises() -> List[Tuple[str, str, str]]:
    """
    :return: 경제 위기 리스트
            start date, end date, crisis 이름
    :rtype: List[Tuple[str, str, str]]
    """
    return [
        ("1983-09-24", "1983-10-17", "검은 토요일"),
        ("1987-07-19", "1988-01-31", "검은 월요일"),
        ("1997-01-01", "1997-12-31", "동 아시아 외환 위기"),
        ("2000-01-01", "2001-03-30", "IT 버블"),
        ("2001-09-11", "2001-12-31", "미국 911 테러"),
        ("2007-12-01", "2009-03-30", "서브 프라임 모기지"),
        ("2010-03-01", "2011-11-01", "유럽 금융 위기"),
        ("2015-08-11", "2016-03-01", "위완화 평가 절하 발표"),
        ("2020-02-21", "2020-03-23", "우한 폐렴 전설의 시작"),
        ("2021-09-18", "2021-10-01", "헝다 그룹 파산"),
        ("2022-02-24", "2022-03-01", "러시아 우크라이나 침공"),
    ]


def plt_year_format() -> Tuple[YearLocator, DateFormatter]:
    """
    :return:
    :rtype:
    """
    return dates.YearLocator(), dates.DateFormatter("%Y")


def plt_year_month_format() -> Tuple[MonthLocator, DateFormatter]:
    """
    :return:
    :rtype:
    """
    return dates.MonthLocator(), dates.DateFormatter("%Y-%M")


# def plt_path(filedir: str, filename: str):
#     path = os.path.join(MEDIA_ROOT, 'plt')
#     validate_path(path)
#
#     path = os.path.join(path, filedir)
#     validate_path(path)
#
#     return os.path.join(path, (filename + '.png'))


def plt_colors(no) -> str:
    """
    :return: 파랑 휴지 줄까? 빨간 휴지 줄까?
    """
    colors = ["blue", "green", "red", "cyan", "magenta", "yellow"]
    return colors[no % len(colors)]


class DataFrameConverter:
    @classmethod
    def stock_price_to_dataframe(
        cls,
        stock_prices: List[StockPrice],
        standardization: bool = False,
        normalization: bool = False,
        earning_ratio: bool = False,
    ) -> DataFrame:
        """
        :param stock_prices: StockPrice Entity
        :param standardization: Do 표준화
        :param normalization: Do 정규화
        :param earning_ratio: Do 수익률
        :return: DataFrame
        :rtype: DataFrame
        """
        if standardization and normalization:
            raise InvalidConvertOption(
                "Invalid argument standardization and normalization can't set true"
            )

        dataframe = pd.DataFrame(
            [price.price_close for price in stock_prices],
            index=[price.date for price in stock_prices],
            columns=["Price"],
        )

        if standardization:
            return standardize(dataframe)
        if normalization:
            return normalize(dataframe)
        if earning_ratio:
            return earning_rate(dataframe)
        return dataframe

    @classmethod
    def index_price_to_dataframe(
        cls,
        index_prices: List[IndexPrice],
        standardization: bool = False,
        normalization: bool = False,
        earning_ratio: bool = False,
    ) -> DataFrame:
        if standardization and normalization:
            raise InvalidConvertOption(
                "Invalid argument standardization and normalization can't set true"
            )

        dataframe = pd.DataFrame(
            [price.price_close for price in index_prices],
            index=[price.date for price in index_prices],
            columns=["Price"],
        )

        if standardization:
            return standardize(dataframe)
        if normalization:
            return normalize(dataframe)
        if earning_ratio:
            return earning_rate(dataframe)
        return dataframe


def earning_rate(dataframe: DataFrame) -> DataFrame:
    """
    수익률
    :return: 수익률
    """
    df = (dataframe / dataframe.iloc[0]) - Decimal(1.0)
    return df


def standardize(dataframe: DataFrame) -> DataFrame:
    """
    정규화, 표준화 https://bskyvision.com/849
    :return: 표준화
    """
    dataframe["Price"] = pd.to_numeric(dataframe["Price"])
    mean, std = dataframe.mean(axis=0), dataframe.std(axis=0)
    return (dataframe["Price"] - mean["Price"]) / std["Price"]


def normalize(dataframe: DataFrame) -> DataFrame:
    """
    정규화, 표준화 https://bskyvision.com/849
    :return: 정규화
    :rtype:
    """
    max_v, min_v = dataframe.max(axis=0), dataframe.min(axis=0)
    return (dataframe["Price"] - min_v["Price"]) / (max_v["Price"] - min_v["Price"])
