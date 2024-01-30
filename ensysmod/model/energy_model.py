from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefDataset

if TYPE_CHECKING:
    from ensysmod.model.energy_model_optimization import EnergyModelOptimization
    from ensysmod.model.energy_model_override import EnergyModelOverride


class EnergyModel(RefDataset, Base):
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str | None]

    # relationships
    override_parameters: Mapped[list["EnergyModelOverride"] | None] = relationship(back_populates="model", cascade="all, delete-orphan")
    optimization_parameters: Mapped["EnergyModelOptimization | None"] = relationship(back_populates="model", cascade="all, delete-orphan")

    # table constraints
    __table_args__ = (UniqueConstraint("ref_dataset", "name", name="_model_name_dataset_uc"),)
