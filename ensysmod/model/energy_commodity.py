from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefDataset


class EnergyCommodity(RefDataset, Base):
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]
    unit: Mapped[str]

    # table constraints
    __table_args__ = (UniqueConstraint("ref_dataset", "name", name="_commodity_name_dataset_uc"),)
