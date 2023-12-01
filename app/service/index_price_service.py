from datetime import datetime
from typing import List

from pandas import DataFrame
from sqlalchemy.exc import NoResultFound

from app.database import IndexPrice, Index
from app.exceptions import IndexNotFound
from app.service.base_service import BaseService
from app.service.index_service import IndexService
from app.vo import Price


class IndexPriceService(BaseService):
    index_service: IndexService = IndexService()

    def create(self, index_price: IndexPrice) -> IndexPrice:
        try:
            self.session.add(index_price)
            self.session.commit() if not self.test_mode else None
            return index_price

        except Exception as e:
            self.session.rollback()
            raise e

    def create_all_with_dataframe(self, dataframe: DataFrame, index: Index):
        index_prices = [
            IndexPrice(
                index.id,
                Price(
                    data["Open"],
                    data["Close"],
                    data["High"],
                    data["Low"],
                    data["Change"],
                ),
                date.strftime("%y-%m-%d"),
            )
            for date, data in dataframe.iterrows()
            if not self.is_exist_index_price(index.id, date.strftime("%y-%m-%d"))
        ]
        self.create_all(index_prices)

    def create_all(self, index_prices: List[IndexPrice]):
        try:
            self.session.add_all(index_prices)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def is_exist_index_price(self, index_id: int, date: str) -> bool:
        try:
            self.session.query(IndexPrice).filter(
                IndexPrice.index_id == index_id, IndexPrice.date == date
            ).one()
            return True
        except NoResultFound:
            return False

    def get_price_list(
        self, index_name: str, start_date: str, end_date: str
    ) -> List[IndexPrice]:
        try:
            return (
                self.session.query(
                    IndexPrice.date, IndexPrice.price_close, Index.index_name
                )
                .join(Index)
                .filter(
                    Index.index_name == index_name,
                    IndexPrice.date >= start_date,
                    IndexPrice.date <= end_date,
                )
                .order_by(IndexPrice.date)
                .all()
            )
        except Exception as e:
            raise e
