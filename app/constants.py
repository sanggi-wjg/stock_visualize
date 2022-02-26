# Database
import os

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
    'USD/KRW',  # 환율
    'DJI',  # 다우 존스
    'US500',  # S&P 500
    'KS11',  # kospi
]
