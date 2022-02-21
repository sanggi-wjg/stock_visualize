import datetime

from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Numeric, Date, UniqueConstraint

from app.exceptions import MarketException
from app.vo import Price

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
        if name not in ['KOSPI', 'KOSDAQ', 'TEST']:
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


Base.metadata.create_all(engine)
Sess = sessionmaker(bind = engine)


def session_factory() -> Session:
    return Sess()
