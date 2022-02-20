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

    def create(self, market: Market, stock_code: str, stock_name: str) -> Stock:
        try:
            stock = Stock(market.id, stock_code, stock_name)
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

    def get_equal_name(self, stock_name: str):
        try:
            return self.session.query(Stock).filter(Stock.stock_name == stock_name).one()
        except NoResultFound:
            raise StockNotFound(f"Stock({stock_name}) not found")

    def delete_equal(self, stock_name: str):
        stocks = self.session.query(Stock).filter(Stock.stock_name == stock_name).all()
        try:
            for stocks in stocks:
                self.session.delete(stocks)

        except Exception as e:
            self.session.rollback()
            raise e
        self.session.commit()
