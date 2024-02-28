from sqlalchemy.orm import Mapped, mapped_column

from ensysmod.database.base_class import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
