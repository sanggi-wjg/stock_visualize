import datetime
import os
from decimal import Decimal
from typing import List

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    Session,
    DeclarativeBase,
    mapped_column,
    Mapped,
)
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Date,
    UniqueConstraint,
)

from app.constant import ALLOW_MARKETS, ALLOW_INDEXES
from app.exception import MarketException, IndexException
from app.model.price import Price


DATABASE = {
    "ENGINE": os.environ.get("DATABASE_ENGINE", "mysql"),
    "NAME": "stock",
    "USER": "root",
    "PASSWORD": "rootroot",
    "HOST": "localhost",
    "PORT": 33061,
}


def get_database_dsn() -> str:
    if DATABASE["ENGINE"] == "mysql":
        return f"mysql+pymysql://{DATABASE['USER']}:{DATABASE['PASSWORD']}@{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['NAME']}"
    elif DATABASE["ENGINE"] == "sqlite":
        return "sqlite:///:memory:"
    else:
        raise Exception(f"not implemented db_engine:{DATABASE['ENGINE']}")


def create_engine_factory():
    if DATABASE["ENGINE"] == "mysql":
        return create_engine(
            get_database_dsn(), isolation_level="REPEATABLE READ", echo=False
        )
    elif DATABASE["ENGINE"] == "sqlite":
        return create_engine(DATABASE["ENGINE"])
    else:
        raise Exception(f"not allowed database engine:{DATABASE['ENGINE']}")


engine = create_engine_factory()
# Base = declarative_base()


class Base(DeclarativeBase):
    pass


class Market(Base):
    __tablename__ = "market"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # 역방향 relation
    stocks: Mapped[List["Stock"]] = relationship("Stock", back_populates="market")

    def __repr__(self):
        return f"<Market(id={self.id} name={self.market_name})>"

    def __init__(self, name: str):
        self.market_name = self.clean_market_name(name.upper())

    def clean_market_name(self, name: str):
        if name not in ALLOW_MARKETS:
            raise MarketException(f"Market({name}) is not allowed")

        return name


class Stock(Base):
    __tablename__ = "stock"
    __table_args__ = (UniqueConstraint("code", "name", name="unq_stock_001_code_name"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    code: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )

    # 정방향 relation
    market_id: Mapped[int] = mapped_column(Integer, ForeignKey("market.id"))
    market: Mapped["Market"] = relationship("Market", back_populates="stocks")

    # 역방향 relation
    prices: Mapped[List["StockPrice"]] = relationship(
        "StockPrice", back_populates="stock"
    )

    def __repr__(self):
        return f"<Stock(id={self.id} market={self.market_id} name={self.stock_name})>"

    def __init__(self, market_id: int, stock_code: str, stock_name: str):
        self.market_id = market_id
        self.stock_code = stock_code
        self.stock_name = stock_name


class StockPrice(Base):
    __tablename__ = "stock_price"
    __table_args__ = (
        UniqueConstraint("stock_id", "date", name="unq_stock_price_001_stock_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    date: Mapped[datetime] = mapped_column(Date(), nullable=False)
    price_open: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_close: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_high: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_low: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_change: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)

    # 정방향 relation
    stock_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("stock.id"), nullable=False
    )
    stock: Mapped["Stock"] = relationship("Stock", back_populates="prices")

    def __repr__(self):
        return f"<StockPrice(id={self.id} stock_id={self.stock_id} date={self.date} close={self.price_close})>"

    def __init__(self, stock_id: int, price: "Price", date: str):
        self.stock_id = stock_id
        self.price_open = price.open
        self.price_close = price.close
        self.price_high = price.high
        self.price_low = price.low
        self.price_change = price.change
        self.date = date


class Index(Base):
    __tablename__ = "index"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # 역방향 relation
    prices: Mapped[List["IndexPrice"]] = relationship(
        "IndexPrice", back_populates="index"
    )

    def __repr__(self):
        return f"<Index(id={self.id} index_name={self.index_name})>"

    def __init__(self, name: str):
        self.index_name = self.clean_index_name(name.upper())

    def clean_index_name(self, name: str):
        if name not in ALLOW_INDEXES:
            raise IndexException(f"Index({name}) is not allowed")
        return name


class IndexPrice(Base):
    __tablename__ = "index_price"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement="auto")
    date: Mapped[datetime] = mapped_column(Date(), nullable=False)
    price_open: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_close: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_high: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_low: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    price_change: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)

    # 정방향 relation
    index_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("indexe.id"), nullable=False
    )
    index: Mapped["Index"] = relationship("Index", back_populates="prices")

    def __repr__(self):
        return f"<IndexPrice(id={self.id} index_id={self.index_id} date={self.date} close={self.price_close})>"

    def __init__(self, index_id: int, price: "Price", date: str):
        self.index_id = index_id
        self.price_open = price.open
        self.price_close = price.close
        self.price_high = price.high
        self.price_low = price.low
        self.price_change = price.change
        self.date = date


Base.metadata.create_all(engine)


def session_factory() -> Session:
    return Session(bind=engine)
