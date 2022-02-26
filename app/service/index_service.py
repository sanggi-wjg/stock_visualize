from app.database import Index
from app.service.base_service import BaseService


class IndexService(BaseService):

    def create(self, index: Index) -> Index:
        try:
            self.session.add(index)
            self.session.commit() if not self.test_mode else None
            return index

        except Exception as e:
            self.session.rollback()
            raise e
