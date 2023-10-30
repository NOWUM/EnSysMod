import re
from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """
    Base class for all database models
    """
    id: Any
    __name__: str
    # TODO https://sqlalche.me/e/20/zlpr
    __allow_unmapped__ = True

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(self) -> str:
        return re.sub(r'(?<!^)(?=[A-Z])', '_', self.__name__).lower()
