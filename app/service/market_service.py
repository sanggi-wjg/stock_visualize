from typing import List

from sqlalchemy.exc import NoResultFound

from app.database import session_factory, Market, Stock
from app.exceptions import MarketNotFound


class MarketService:

    def create(self, market_name: str) -> Market:
        with session_factory() as session:
            try:
                market = Market(market_name.upper())
                session.add(market)
                session.commit()
                return market

            except Exception as e:
                session.rollback()
                raise e

    def lists(self) -> List[Market]:
        with session_factory() as session:
            return session.query(Market).all()

    def get_or_create(self, market_name: str) -> Market:
        with session_factory() as session:
            try:
                market = session.query(Market).filter(Market.market_name == market_name.upper()).one()
                return market

            except NoResultFound:
                try:
                    market = Market(market_name)
                    session.add(market)
                    session.commit()
                    return market

                except Exception as e:
                    session.rollback()
                    raise e

    def delete_equal(self, market_name: str):
        with session_factory() as session:
            markets = session.query(Market).filter(Market.market_name == market_name.upper()).all()
            try:
                for market in markets:
                    session.delete(market)

            except Exception as e:
                session.rollback()
                raise e
            session.commit()


class StockService:

    def create(self, market_name: str, stock_code: str, stock_name: str) -> Stock:
        with session_factory() as session:
            try:
                market = session.query(Market).filter(Market.market_name == market_name.upper()).one()

            except NoResultFound:
                try:
                    market = Market(market_name)
                    session.add(market)

                except Exception as e:
                    session.rollback()
                    raise e

            else:
                try:
                    stock = Stock(market.id, stock_code, stock_name)
                    session.add(stock)
                    session.commit()
                    return stock

                except Exception as e:
                    session.rollback()
                    raise e

    def is_exist_equal(self, stock_name: str) -> bool:
        with session_factory() as session:
            try:
                session.query(Stock).filter(Stock.stock_name == stock_name).one()
                return True
            except NoResultFound:
                return False

    def delete_equal(self, stock_name: str):
        with session_factory() as session:
            stocks = session.query(Stock).filter(Stock.stock_name == stock_name).all()
            try:
                for stocks in stocks:
                    session.delete(stocks)

            except Exception as e:
                session.rollback()
                raise e
            session.commit()
