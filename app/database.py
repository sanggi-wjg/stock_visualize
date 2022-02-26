import datetime

from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric, Date, UniqueConstraint

from app.constants import ALLOW_MARKETS, DATABASE_DSN, ALLOW_INDEXES, DATABASE_ENGINE
from app.exceptions import MarketException, IndexException
from app.vo import Price


def create_engine_factory():

    if DATABASE_ENGINE == 'mysql':
        return create_engine(DATABASE_DSN, isolation_level = 'REPEATABLE READ', echo = False)
    elif DATABASE_ENGINE == 'sqlite':
        return create_engine(DATABASE_DSN)
    else:
        raise Exception(f"not allowed database engine:{DATABASE_ENGINE}")


engine = create_engine_factory()
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
        if name not in ALLOW_MARKETS:
            raise MarketException(f"Market({name}) is not allowed")

        return name


class Stock(Base):
    __tablename__ = 'stocks'
    __table_args__ = (
        UniqueConstraint('stock_code', 'stock_name', name = 'unique_stocks_stock'),
    )

    id = Column(Integer, primary_key = True, autoincrement = "auto")

    # 정방향 relation
    market_id = Column(Integer, ForeignKey("markets.id"))
    market = relationship("Market", back_populates = "stocks")

    # 역방향 relation
    stock_prices = relationship("StockPrice", back_populates = "stock")

    stock_code = Column(String(50), unique = True, nullable = False)
    stock_name = Column(String(50), unique = True, nullable = False, index = True)

    def __repr__(self):
        return f"<Stock(id={self.id} market={self.market_id} name={self.stock_name})>"

    def __init__(self, market_id: int, stock_code: str, stock_name: str):
        self.market_id = market_id
        self.stock_code = stock_code
        self.stock_name = stock_name


class StockPrice(Base):
    __tablename__ = 'stock_prices'
    __table_args__ = (
        UniqueConstraint('stock_id', 'date', name = 'unique_stock_price_stock_date'),
    )

    id = Column(Integer, primary_key = True, autoincrement = "auto")

    # 정방향 relation
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable = False)
    stock = relationship("Stock", back_populates = "stock_prices")

    price_open = Column(Numeric(10, 2), nullable = False)
    price_close = Column(Numeric(10, 2), nullable = False)
    price_high = Column(Numeric(10, 2), nullable = False)
    price_low = Column(Numeric(10, 2), nullable = False)
    price_change = Column(Numeric(10, 6), nullable = False)

    date = Column(Date(), nullable = False)

    def __repr__(self):
        return f"<StockPrice(id={self.id} stock_id={self.stock_id} date={self.date} close={self.price_close})>"

    def __init__(self, stock_id: int, price: 'Price', date: str):
        self.stock_id = stock_id
        self.price_open = price.open
        self.price_close = price.close
        self.price_high = price.high
        self.price_low = price.low
        self.price_change = price.change
        self.date = date


class Index(Base):
    __tablename__ = 'indexes'

    id = Column(Integer, primary_key = True, autoincrement = "auto")

    # 역방향 relation
    index_prices = relationship("IndexPrice", back_populates = "index")

    index_name = Column(String(50), unique = True, nullable = False)

    def __repr__(self):
        return f"<Index(id={self.id} index_name={self.index_name})>"

    def __init__(self, name: str):
        self.index_name = self.clean_index_name(name.upper())

    def clean_index_name(self, name: str):
        if name not in ALLOW_INDEXES:
            raise IndexException(f"Index({name}) is not allowed")
        return name


class IndexPrice(Base):
    __tablename__ = 'index_prices'

    id = Column(Integer, primary_key = True, autoincrement = "auto")

    # 정방향 relation
    index_id = Column(Integer, ForeignKey("indexes.id"), nullable = False)
    index = relationship("Index", back_populates = "index_prices")

    price_open = Column(Numeric(10, 2), nullable = False)
    price_close = Column(Numeric(10, 2), nullable = False)
    price_high = Column(Numeric(10, 2), nullable = False)
    price_low = Column(Numeric(10, 2), nullable = False)
    price_change = Column(Numeric(10, 6), nullable = False)

    date = Column(Date(), nullable = False)

    def __repr__(self):
        return f"<IndexPrice(id={self.id} index_id={self.index_id} date={self.date} close={self.price_close})>"

    def __init__(self, index_id: int, price: 'Price', date: str):
        self.index_id = index_id
        self.price_open = price.open
        self.price_close = price.close
        self.price_high = price.high
        self.price_low = price.low
        self.price_change = price.change
        self.date = date


Base.metadata.create_all(engine)
Sess = sessionmaker(bind = engine)


def session_factory() -> Session:
    return Sess()
