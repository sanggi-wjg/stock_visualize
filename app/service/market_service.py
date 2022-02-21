from typing import List

from sqlalchemy.exc import NoResultFound

from app.database import session_factory, Market


class MarketService:

    def __init__(self):
        self.session = session_factory()

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()

    def create(self, market: Market) -> Market:
        try:
            self.session.add(market)
            self.session.commit()
            return market

        except Exception as e:
            self.session.rollback()
            raise e

    def lists(self) -> List[Market]:
        return self.session.query(Market).all()

    def get_equal(self, market_name: str) -> Market:
        return self.session.query(Market).filter(Market.market_name == market_name.upper()).one()

    def get_or_create(self, market_name: str) -> Market:
        try:
            return self.session.query(Market).filter(Market.market_name == market_name.upper()).one()

        except NoResultFound:
            try:
                market = Market(market_name)
                self.session.add(market)
                self.session.commit()
                return market

            except Exception as e:
                self.session.rollback()
                raise e

    def delete_equal(self, market_name: str):
        markets = self.session.query(Market).filter(Market.market_name == market_name.upper()).all()
        try:
            for market in markets:
                self.session.delete(market)
        except Exception as e:
            self.session.rollback()
            raise e
        self.session.commit()
