from typing import List

from pandas import DataFrame
from sqlalchemy.exc import NoResultFound

from app.database import session_factory, StockPrice, Stock
from app.exceptions import StockNotFound
from app.service.stock_service import StockService
from app.vo import Price


class StockPriceService:

    def __init__(self):
        self.session = session_factory()
        self.stock_service = StockService()

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()

    def create(self, stock_price: StockPrice) -> StockPrice:
        try:
            self.session.add(stock_price)
            self.session.commit()
            return stock_price

        except Exception as e:
            self.session.rollback()
            raise e

    def create_dataframe(self, dataframe: DataFrame):
        try:
            stock = self.stock_service.get_equal_code("005930")
        except StockNotFound as e:
            raise e
        else:
            stock_prices = [
                StockPrice(
                    stock.id, Price(data['Open'], data['Close'], data['High'], data['Low'], data['Change']), date.strftime('%y-%m-%d')
                )
                for date, data in dataframe.iterrows()
                if not self.is_exist_stock_price(stock.id, date.strftime('%y-%m-%d'))
            ]
            self.create_all(stock_prices)

    def create_all(self, stock_prices: List[StockPrice]):
        try:
            self.session.add_all(stock_prices)
            self.session.commit()

        except Exception as e:
            self.session.rollback()
            raise e

    def get_or_create(self):
        pass

    def is_exist_stock_price(self, stock_id: int, date: str):
        try:
            self.session.query(StockPrice).filter(StockPrice.stock_id == stock_id, StockPrice.date == date).one()
            return True
        except NoResultFound:
            return False

    def delete_equal_stock(self, stock_name: str):
        try:
            stock = self.stock_service.get_equal_name(stock_name)
            stock_prices = self.session.query(StockPrice).filter(StockPrice.stock_id == stock.id).all()

            for price in stock_prices:
                self.session.delete(price)

        except Exception as e:
            self.session.rollback()
            raise e
        self.session.commit()
