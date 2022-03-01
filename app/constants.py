# Database
import os
from typing import List, Dict, Tuple

DATABASE = {
    'NAME'    : "Sample",
    "USER"    : "root",
    "PASSWORD": "rootroot",
    'HOST'    : '192.168.10.151',
    'PORT'    : 33061,
}


def get_database_dsn() -> str:
    if DATABASE_ENGINE == "mysql":
        return f"mysql+pymysql://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['NAME']}"
    elif DATABASE_ENGINE == "sqlite":
        return "sqlite:///:memory:"
    else:
        raise Exception(f"not implemented db_engine:{DATABASE_ENGINE}")


DATABASE_ENGINE = os.environ.get("DATABASE_ENGINE", "mysql")
DATABASE_DSN = get_database_dsn()

# Setting Constants
ALLOW_MARKETS = ['KOSPI', 'KOSDAQ', 'TEST']
ALLOW_INDEXES = [
    # 환율
    'USD/KRW',

    # 미국
    'DJI',  # 다우 존스
    'US500',  # S&P 500
    'IXIC',  # NASDAQ
    'VIX',  # 변동성 지수 (Greed And Fear)

    # 한국
    'KS11',  # KOSPI
    'KS100',  # KOSPI 100
    'KS200',  # KOSPI 200
    'KQ11',  # KOSDAQ

    # 선물
    'NG',  # 천연 가스
    'GC',  # 금
    'SI',  # 은
    'HG',  # 구리
    'CL',  # WTI
]
