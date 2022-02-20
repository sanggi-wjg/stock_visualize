from app.database import session_factory, StockPrice, Stock, Price
from app.service.stock_service import StockService


class StockPriceService:

    def __init__(self):
        self.session = session_factory()
        self.stock_service = StockService()

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()

    def create(self, stock: Stock, price: Price, date: str) -> StockPrice:
        try:
            stock_price = StockPrice(
                stock.id,
                price.open, price.close, price.high, price.low,
                date
            )
            self.session.add(stock_price)
            self.session.commit()
            return stock_price

        except Exception as e:
            self.session.rollback()
            raise e

    def get_or_create(self):
        pass

    def delete_equal_stock(self, stock_name: str):
        try:
            stock = self.stock_service.get_equal_name(stock_name)
            stock_prices = self.session.query(StockPrice).filter(StockPrice.stock_id == stock.id).all()

            for price in stock_prices:
                self.session.delete(price)

        except Exception as e:
            self.session.rollback()
        self.session.commit()
