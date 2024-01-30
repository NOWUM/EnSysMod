from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponentUnique, RefDataset

if TYPE_CHECKING:
    from ensysmod.model.energy_conversion_factor import EnergyConversionFactor


class EnergyConversion(RefComponentUnique, RefDataset, Base):
    physical_unit: Mapped[str]

    # relationships
    conversion_factors: Mapped[list[EnergyConversionFactor]] = relationship(back_populates="conversion", cascade="all, delete-orphan")
