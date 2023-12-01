from app.database import session_factory
from app.util import get_logger

log = get_logger()


class BaseRepository:
    def __init__(self, test_mode: bool = False):
        self.session = session_factory()
        self.test_mode = test_mode
        if self.test_mode:
            log.error(
                f"Current Service test_mode is `{self.__class__}`. Not allowed commit."
            )

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()
