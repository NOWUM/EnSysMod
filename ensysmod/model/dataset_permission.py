from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefDataset

if TYPE_CHECKING:
    from ensysmod.model import User


class DatasetPermission(RefDataset, Base):
    ref_user: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    allow_usage: Mapped[bool]
    allow_modification: Mapped[bool]
    allow_permission_grant: Mapped[bool]
    allow_permission_revoke: Mapped[bool]

    # relationships
    user: Mapped[User] = relationship()

    # table constraints
    __table_args__ = (UniqueConstraint("ref_dataset", "ref_user", name="_dataset_user_uc"),)
