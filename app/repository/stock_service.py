from typing import List

from sqlalchemy.exc import NoResultFound

from app.database import Stock, Market, session_factory
from app.exceptions import StockNotFound


class StockService:
    def __init__(self):
        self.session = session_factory()

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()

    def create(self, stock: Stock) -> Stock:
        try:
            self.session.add(stock)
            self.session.commit()
            return stock

        except Exception as e:
            self.session.rollback()
            raise e

    def is_exist_equal(self, stock_name: str) -> bool:
        try:
            self.session.query(Stock).filter(Stock.stock_name == stock_name).one()
            return True
        except NoResultFound:
            return False

    def get_equal_name(self, stock_name: str) -> Stock:
        try:
            return (
                self.session.query(Stock).filter(Stock.stock_name == stock_name).one()
            )
        except NoResultFound:
            raise StockNotFound(f"Stock({stock_name}) not found")

    def get_equal_code(self, stock_code: str) -> Stock:
        try:
            return (
                self.session.query(Stock).filter(Stock.stock_code == stock_code).one()
            )
        except NoResultFound:
            raise StockNotFound(f"Stock({stock_code}) not found")

    def lists(self) -> List[Stock]:
        return self.session.query(Stock).all()

    def delete_equal(self, stock_name: str):
        stocks = self.session.query(Stock).filter(Stock.stock_name == stock_name).all()
        try:
            for stocks in stocks:
                self.session.delete(stocks)

        except Exception as e:
            self.session.rollback()
            raise e
        self.session.commit()
