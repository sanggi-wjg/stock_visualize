from app.colorful import red
from app.database import session_factory


class BaseService:
    def __init__(self, test_mode: bool = False):
        self.session = session_factory()
        self.test_mode = test_mode
        if self.test_mode:
            red(f"Current Service test_mode is `{self.__class__}`. Not allowed commit.")

    def __del__(self):
        self.close()

    def close(self):
        self.session.close()
