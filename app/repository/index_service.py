from typing import List

from sqlalchemy.exc import NoResultFound

from app.database import Index
from app.exceptions import IndexNotFound
from app.repository.base_service import BaseService


class IndexService(BaseService):
    def create(self, index: Index) -> Index:
        try:
            self.session.add(index)
            self.session.commit() if not self.test_mode else None
            return index

        except Exception as e:
            self.session.rollback()
            raise e

    def get_or_create(self, index_name: str) -> Index:
        try:
            return (
                self.session.query(Index)
                .filter(Index.index_name == index_name.upper())
                .one()
            )

        except NoResultFound:
            return self.create(Index(index_name))

    def get_equal_name(self, index_name: str) -> Index:
        try:
            return (
                self.session.query(Index).filter(Index.index_name == index_name).one()
            )
        except NoResultFound:
            raise IndexNotFound(f"Index({index_name}) not found")

    def lists(self) -> List[Index]:
        return self.session.query(Index).order_by(Index.id).all()
