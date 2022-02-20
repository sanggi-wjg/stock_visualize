import datetime

from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey

from app.exceptions import MarketException

engine = create_engine(
    "mysql+pymysql://root:rootroot@192.168.10.151:33061/Sample",
    isolation_level = 'REPEATABLE READ', echo = False
)

Base = declarative_base()


class Market(Base):
    __tablename__ = 'markets'

    id = Column(Integer, primary_key = True, autoincrement = "auto")
    market_name = Column(String(50), unique = True, nullable = False)
    created_at = Column(DateTime(), default = datetime.datetime.utcnow())

    # 역방향 relation
    stocks = relationship("Stock", back_populates = "market")

    def __repr__(self):
        return f"<Market(id={self.id} name={self.market_name})>"

    def __init__(self, name: str):
        self.market_name = self.clean_market_name(name.upper())

    def clean_market_name(self, name: str):
        if name not in ['KOSPI', 'KOSDAQ']:
            raise MarketException(f"Market({name}) is not allowed")

        return name


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key = True, autoincrement = "auto")

    # 정방향 relation
    market_id = Column(Integer, ForeignKey("markets.id"))
    market = relationship("Market", back_populates = "stocks")

    stock_code = Column(String(50), unique = True, nullable = False)
    stock_name = Column(String(50), unique = True, nullable = False, index = True)

    def __repr__(self):
        return f"<Stock(id={self.id} market={self.market_id} name={self.stock_name})>"

    def __init__(self, market_id: int, stock_code: str, stock_name: str):
        self.market_id = market_id
        self.stock_code = stock_code
        self.stock_name = stock_name


Base.metadata.create_all(engine)
Sess = sessionmaker(bind = engine)


def session_factory() -> Session:
    return Sess()
