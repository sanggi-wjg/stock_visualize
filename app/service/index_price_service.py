from app.database import IndexPrice
from app.service.base_service import BaseService


class IndexPriceService(BaseService):

    def create(self, index_price: IndexPrice) -> IndexPrice:
        try:
            self.session.add(index_price)
            self.session.commit() if not self.test_mode else None
            return index_price

        except Exception as e:
            self.session.rollback()
            raise e
