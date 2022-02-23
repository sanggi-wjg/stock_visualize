from typing import List, Tuple

from matplotlib import dates
from matplotlib.dates import DateFormatter, YearLocator, MonthLocator
from pandas import DataFrame


def financial_crisis_list() -> List[Tuple[str, str, str]]:
    """
    :return: 경제 위기 리스트
    :rtype: List[Tuple[str, str, str]]
    """
    return [
        ('1983-09-24', '1983-10-17', '검은 토요일'),
        ('1987-07-19', '1988-01-31', '검은 월요일'),
        ('1997-01-01', '1997-12-31', '동아시아 외환 위기'),
        ('2000-01-01', '2001-03-30', 'IT 버블'),
        ('2001-09-11', '2001-12-31', '미국 911 테러'),
        ('2007-12-01', '2009-03-30', '서브 프라임 모기지'),
        ('2010-03-01', '2011-11-01', '유럽 금융 위기'),
        ('2015-08-11', '2016-03-01', '위완화 평가 절하 발표'),
        ('2020-03-01', '2020-04-01', '우한 폐렴'),
    ]


def plt_year_format() -> Tuple[YearLocator, DateFormatter]:
    """
    :return:
    :rtype:
    """
    return dates.YearLocator(), dates.DateFormatter('%Y')


def plt_year_month_format() -> Tuple[MonthLocator, DateFormatter]:
    """
    :return:
    :rtype:
    """
    return dates.MonthLocator(), dates.DateFormatter('%Y-%M')


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
    파랑색 휴지 줄까? 빨간색 휴지 줄까?
    :param no:
    :type no:
    :return:
    :rtype:
    """
    colors = ['blue', 'red', 'green', 'cyan', 'magenta', 'yellow']
    return colors[no % len(colors)]


def standardize(dataframe: DataFrame, column: str) -> DataFrame:
    """
    정규화, 표준화 https://bskyvision.com/849
    표준화
    :param dataframe:
    :type dataframe:
    :param column:
    :type column:
    :return:
    :rtype:
    """
    mean, std = dataframe.mean(axis = 0), dataframe.std(axis = 0)
    return (dataframe[column] - mean[column]) / std[column]


def normalize(dataframe: DataFrame, column: str) -> DataFrame:
    """
    정규화, 표준화 https://bskyvision.com/849
    정규화
    :param dataframe:
    :type dataframe:
    :param column:
    :type column:
    :return:
    :rtype:
    """
    max_v, min_v = dataframe.max(axis = 0), dataframe.min(axis = 0)
    return (dataframe[column] - min_v[column]) / (max_v[column] - min_v[column])
