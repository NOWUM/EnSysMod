import re

from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all database models
    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Generate __tablename__ automatically
    @declared_attr.directive
    def __tablename__(self) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", self.__name__).lower()
