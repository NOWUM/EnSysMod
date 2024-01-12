from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ensysmod.database.base_class import Base
from ensysmod.database.ref_base_class import RefComponentUnique, RefDataset

if TYPE_CHECKING:
    from model.energy_commodity import EnergyCommodity
    from model.energy_conversion_factor import EnergyConversionFactor


class EnergyConversion(RefComponentUnique, RefDataset, Base):
    ref_commodity_unit: Mapped[int] = mapped_column(ForeignKey("energy_commodity.id"))

    # relationships
    commodity_unit: Mapped[EnergyCommodity] = relationship()
    conversion_factors: Mapped[list[EnergyConversionFactor]] = relationship(back_populates="conversion")
